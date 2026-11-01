import json
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone

from .models import CampaignScenario, CampaignQuestion, CallLog, CallTranscript, ScheduledCall, TelephonyConfig
from .forms import TriggerCallForm, CampaignForm, ScheduleForm, TelephonyConfigForm
from .services.twilio_service import TwilioVoiceService
from .services.retell_service import RetellAIService
from .services.vapi_service import VapiVoiceService
from .services.mock_service import MockCallService

def dashboard_view(request):
    scenarios = CampaignScenario.objects.all().prefetch_related('questions')
    logs = CallLog.objects.all().prefetch_related('transcripts')[:50]
    schedules = ScheduledCall.objects.filter(status='Pending')
    config = TelephonyConfig.get_config()

    total_calls = CallLog.objects.count()
    completed_calls = CallLog.objects.filter(status='Completed').count()
    success_rate = round((completed_calls / total_calls) * 100) if total_calls > 0 else 100

    positive_calls = CallLog.objects.filter(sentiment='Positive').count()
    positive_rate = round((positive_calls / total_calls) * 100) if total_calls > 0 else 0

    pending_schedules = schedules.count()

    context = {
        'scenarios': scenarios,
        'logs': logs,
        'schedules': schedules,
        'total_calls': total_calls,
        'success_rate': success_rate,
        'positive_rate': positive_rate,
        'pending_schedules': pending_schedules,
        'trigger_form': TriggerCallForm(),
        'config': config,
        'config_form': TelephonyConfigForm(instance=config)
    }

    return render(request, 'assistant/dashboard.html', context)

def save_telephony_config_view(request):
    if request.method == 'POST':
        config = TelephonyConfig.get_config()
        form = TelephonyConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "🔑 Telephony API Keys updated successfully!")
        else:
            messages.error(request, "Error saving Telephony API keys.")
    return redirect('dashboard')

def trigger_call_view(request):
    if request.method == 'POST':
        form = TriggerCallForm(request.POST)
        if form.is_valid():
            scenario_id = form.cleaned_data['scenario_id']
            phone_number = form.cleaned_data['phone_number']
            recipient_name = form.cleaned_data['recipient_name']
            engine = form.cleaned_data['engine']

            scenario = get_object_or_404(CampaignScenario, pk=scenario_id)
            host_url = request.build_absolute_uri('/')[:-1]

            try:
                if engine == 'twilio':
                    service = TwilioVoiceService()
                    log = service.create_phone_call(phone_number, scenario, host_url=host_url)
                    messages.success(request, f"📞 REAL PHONE CALL DIALING! Twilio is calling {phone_number} right now. Please answer your mobile phone!")
                elif engine == 'retell':
                    service = RetellAIService()
                    log = service.create_phone_call(phone_number, scenario)
                    messages.success(request, f"🤖 REAL PHONE CALL DISPATCHED! Retell AI is calling {phone_number} right now!")
                elif engine == 'vapi':
                    service = VapiVoiceService()
                    log = service.create_call(phone_number, scenario)
                    messages.success(request, f"⚡ REAL PHONE CALL DISPATCHED! Vapi Voice AI is calling {phone_number} right now!")
                else:
                    service = MockCallService()
                    log = service.simulate_call(phone_number, scenario, engine_name='Mock Phone Simulator')
                    messages.info(request, f"📱 Phone Call simulated for {scenario.title}! Logs and answers saved in Django DB.")
            except Exception as e:
                messages.error(request, f"⚠️ Real Call Failed: {str(e)}")

            return redirect('dashboard')

    return redirect('dashboard')

@csrf_exempt
def twilio_start_webhook(request):
    """
    Generates TwiML XML instructions when Twilio calls the recipient's mobile phone
    """
    scenario_id = request.GET.get('scenario_id')
    scenario = get_object_or_404(CampaignScenario, pk=scenario_id)

    first_question = scenario.questions.first()
    q_text = first_question.text if first_question else "How are you doing today?"

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{scenario.greeting}</Say>
    <Pause length="1"/>
    <Gather input="speech" timeout="5" action="/webhooks/twilio/gather/?scenario_id={scenario.id}&amp;q_idx=0" method="POST">
        <Say voice="Polly.Joanna">{q_text}</Say>
    </Gather>
</Response>"""
    return HttpResponse(twiml, content_type='text/xml')

@csrf_exempt
def twilio_gather_webhook(request):
    """
    Receives speech transcript from user's mobile phone response, logs it, and speaks next question
    """
    scenario_id = request.GET.get('scenario_id')
    q_idx = int(request.GET.get('q_idx', 0))

    scenario = get_object_or_404(CampaignScenario, pk=scenario_id)
    speech_result = request.POST.get('SpeechResult', 'Speech not recognized')

    # Store transcript in latest in-progress log
    latest_log = CallLog.objects.filter(scenario=scenario, status='In Progress').first()
    if not latest_log:
        latest_log = CallLog.objects.create(
            scenario=scenario,
            title=scenario.title,
            recipient_name=scenario.recipient_name,
            phone_number=scenario.phone_number,
            engine_used='Twilio Real PSTN'
        )

    # Record answer in extracted data
    questions = list(scenario.questions.all())
    if q_idx < len(questions):
        current_q = questions[q_idx]
        latest_log.extracted_data[current_q.key] = speech_result
        CallTranscript.objects.create(call_log=latest_log, speaker='User', text=speech_result)
        latest_log.save()

    # Move to next question or conclude
    next_idx = q_idx + 1
    if next_idx < len(questions):
        next_q = questions[next_idx]
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" timeout="5" action="/webhooks/twilio/gather/?scenario_id={scenario.id}&amp;q_idx={next_idx}" method="POST">
        <Say voice="Polly.Joanna">{next_q.text}</Say>
    </Gather>
</Response>"""
    else:
        latest_log.status = 'Completed'
        latest_log.save()
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{scenario.closing_message or 'Thank you for your responses. Goodbye!'}</Say>
    <Hangup/>
</Response>"""

    return HttpResponse(twiml, content_type='text/xml')

def log_detail_view(request, log_id):
    log = get_object_or_404(CallLog, pk=log_id)
    transcripts = log.transcripts.all()
    return render(request, 'assistant/log_detail.html', {'log': log, 'transcripts': transcripts})

def create_script_view(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            scenario = form.save()
            CampaignQuestion.objects.create(scenario=scenario, text="How would you rate your satisfaction from 1 to 5?", key="satisfaction", response_type="rating", options=["1", "2", "3", "4", "5"], order=0)
            CampaignQuestion.objects.create(scenario=scenario, text="Would you like a follow up text?", key="followup", response_type="yes_no", options=["Yes", "No"], order=1)
            messages.success(request, f"✨ Custom Campaign '{scenario.title}' created!")
            return redirect('dashboard')
    else:
        form = CampaignForm()

    return render(request, 'assistant/script_form.html', {'form': form})

def create_schedule_view(request):
    if request.method == 'POST':
        scenario_id = request.POST.get('scenario_id')
        phone_number = request.POST.get('phone_number', '+1 (555) 000-0000')
        delay_seconds = int(request.POST.get('delay_seconds', 30))

        scenario = get_object_or_404(CampaignScenario, pk=scenario_id)
        scheduled_time = timezone.now() + timezone.timedelta(seconds=delay_seconds)

        ScheduledCall.objects.create(
            scenario=scenario,
            recipient_name=scenario.recipient_name,
            phone_number=phone_number,
            scheduled_time=scheduled_time,
            delay_seconds=delay_seconds,
            status='Pending'
        )
        messages.success(request, f"⏰ Call scheduled to trigger in {delay_seconds} seconds!")
        return redirect('dashboard')

    scenarios = CampaignScenario.objects.all()
    return render(request, 'assistant/schedule_form.html', {'scenarios': scenarios})

def clear_logs_view(request):
    CallLog.objects.all().delete()
    messages.info(request, "Call logs cleared from database.")
    return redirect('dashboard')

def export_logs_json(request):
    logs = list(CallLog.objects.values(
        'call_id', 'title', 'category', 'recipient_name', 'phone_number', 
        'engine_used', 'timestamp', 'duration_seconds', 'status', 'sentiment', 'extracted_data'
    ))
    response = HttpResponse(json.dumps(logs, default=str, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="echocall_logs.json"'
    return response

def export_logs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="echocall_logs.csv"'
    writer = csv.writer(response)
    writer.writerow(['Call ID', 'Timestamp', 'Scenario', 'Recipient', 'Phone', 'Engine', 'Status', 'Sentiment', 'Duration(s)', 'Answers'])

    for log in CallLog.objects.all():
        answers = " | ".join([f"{k}:{v}" for k, v in log.extracted_data.items()])
        writer.writerow([log.call_id, log.timestamp, log.title, log.recipient_name, log.phone_number, log.engine_used, log.status, log.sentiment, log.duration_seconds, answers])

    return response

@csrf_exempt
def webhooks_retell_view(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            call_id = payload.get('call', {}).get('call_id')
            transcript = payload.get('call', {}).get('transcript', '')

            if call_id:
                log, _ = CallLog.objects.get_or_create(call_id=call_id, defaults={'title': 'Retell AI Call', 'recipient_name': 'Mobile User', 'phone_number': '+1 Mobile'})
                log.status = 'Completed'
                log.save()
                CallTranscript.objects.create(call_log=log, speaker='AI', text=transcript or 'Call ended via Retell webhook')

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'status': 'method not allowed'}, status=405)

@csrf_exempt
def webhooks_vapi_view(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            call_id = payload.get('message', {}).get('call', {}).get('id')
            if call_id:
                log, _ = CallLog.objects.get_or_create(call_id=call_id, defaults={'title': 'Vapi Voice Call', 'recipient_name': 'Mobile User', 'phone_number': '+1 Mobile'})
                log.status = 'Completed'
                log.save()

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'status': 'method not allowed'}, status=405)

def machinesense_view(request):
    """
    Renders MachineSense — an AI-powered predictive maintenance dashboard
    integrating live sensor simulation, mini-RAG, prompt engineering, Claude API, and cloud mapping.
    """
    return render(request, 'assistant/machinesense.html')

