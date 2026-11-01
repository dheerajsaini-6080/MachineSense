import uuid
import random

class MockCallService:
    def simulate_call(self, phone_number, scenario, engine_name='mock'):
        from assistant.models import CallLog, CallTranscript

        call_id = f"call-{uuid.uuid4().hex[:8]}"

        # Sample responses per question type
        sample_responses = {
            'yes_no': ['Yes, confirmed!', 'Yes, already completed.', 'No, not yet.'],
            'rating': ['5 out of 5', '4 out of 5', '5/5'],
            'confirmation': ['Confirmed', 'Yes, I will attend.'],
            'open_text': ['Feeling great, no complaints!', 'Package arrived in clean condition.', 'Schedule reminder for 6 PM.']
        }

        extracted = {}
        transcripts = []

        # 1. AI Greeting
        transcripts.append(('AI', scenario.greeting))

        # 2. Q&A Sequence
        for idx, q in enumerate(scenario.questions.all()):
            transcripts.append(('AI', q.text))

            ans_choices = sample_responses.get(q.response_type, ['Yes, confirmed'])
            user_ans = random.choice(ans_choices)

            transcripts.append(('User', user_ans))
            extracted[q.key] = user_ans

        # 3. AI Closing
        transcripts.append(('AI', scenario.closing_message or 'Thank you for your time!'))

        # Determine sentiment
        sentiment = 'Positive'
        if any('no' in str(v).lower() for v in extracted.values()):
            sentiment = 'Neutral'

        # Create CallLog entry in Django DB
        call_log = CallLog.objects.create(
            call_id=call_id,
            scenario=scenario,
            title=scenario.title,
            category=scenario.category,
            recipient_name=scenario.recipient_name or 'Client',
            phone_number=phone_number,
            engine_used=engine_name,
            duration_seconds=random.randint(25, 55),
            status='Completed',
            sentiment=sentiment,
            extracted_data=extracted
        )

        # Create Transcript objects in Django DB
        for speaker, text in transcripts:
            CallTranscript.objects.create(
                call_log=call_log,
                speaker=speaker,
                text=text
            )

        return call_log
