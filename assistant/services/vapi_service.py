import requests
from assistant.models import TelephonyConfig, CallLog, CallTranscript

class VapiVoiceService:
    def create_call(self, phone_number, scenario):
        config = TelephonyConfig.get_config()
        api_key = config.vapi_api_key
        phone_number_id = config.vapi_phone_number_id

        if not api_key:
            raise ValueError("Vapi API Key missing! Click 'Telephony Keys' in navbar to enter your Vapi API key.")

        base_url = 'https://api.vapi.ai'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'type': 'outboundPhoneCall',
            'phoneNumber': phone_number,
            'phoneNumberId': phone_number_id if phone_number_id else None,
            'assistant': {
                'firstMessage': scenario.greeting,
                'model': {
                    'provider': 'openai',
                    'model': 'gpt-4o',
                    'messages': [
                        {
                            'role': 'system',
                            'content': f"You are EchoCall AI making an automated check call for '{scenario.title}'. Ask these questions sequentially: " + 
                                       "; ".join([q.text for q in scenario.questions.all()])
                        }
                    ]
                }
            }
        }

        res = requests.post(f"{base_url}/call", json=payload, headers=headers, timeout=12)
        if res.status_code in [200, 201]:
            data = res.json()
            call_id = data.get('id', f"vapi-{scenario.id}")
            call_log = CallLog.objects.create(
                call_id=call_id,
                scenario=scenario,
                title=scenario.title,
                category=scenario.category,
                recipient_name=scenario.recipient_name,
                phone_number=phone_number,
                engine_used='Vapi Voice Real Call',
                status='In Progress',
                sentiment='Positive',
                extracted_data={'status': 'Real Mobile Call Dispatched via Vapi AI'}
            )
            return call_log
        else:
            err_text = res.json().get('message', res.text)
            raise ValueError(f"Vapi AI Error: {err_text}")
