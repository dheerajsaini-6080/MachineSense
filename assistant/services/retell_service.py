import requests
from assistant.models import TelephonyConfig, CallLog, CallTranscript

class RetellAIService:
    def create_phone_call(self, phone_number, scenario):
        config = TelephonyConfig.get_config()
        api_key = config.retell_api_key
        agent_id = config.retell_agent_id

        if not api_key:
            raise ValueError("Retell API Key missing! Click 'Telephony Keys' in navbar to enter your Retell API key & Agent ID.")

        base_url = 'https://api.retellai.com/v2'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        questions_text = "\n".join([f"- Question {idx+1}: {q.text}" for idx, q in enumerate(scenario.questions.all())])

        payload = {
            'override_agent_id': agent_id if agent_id else None,
            'to_number': phone_number,
            'override_agent_prompt': f"Greeting: {scenario.greeting}\nAsk the following questions sequentially:\n{questions_text}\nClosing: {scenario.closing_message}"
        }

        res = requests.post(f"{base_url}/create-phone-call", json=payload, headers=headers, timeout=12)
        if res.status_code in [200, 201]:
            data = res.json()
            call_id = data.get('call_id', f"retell-{scenario.id}")
            call_log = CallLog.objects.create(
                call_id=call_id,
                scenario=scenario,
                title=scenario.title,
                category=scenario.category,
                recipient_name=scenario.recipient_name,
                phone_number=phone_number,
                engine_used='Retell AI Real Call',
                status='In Progress',
                sentiment='Positive',
                extracted_data={'status': 'Real Mobile Call Dispatched via Retell AI'}
            )
            return call_log
        else:
            err_text = res.json().get('message', res.text)
            raise ValueError(f"Retell AI Error: {err_text}")
