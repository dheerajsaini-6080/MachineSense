import requests
from assistant.models import TelephonyConfig, CallLog, CallTranscript

class TwilioVoiceService:
    def create_phone_call(self, phone_number, scenario, host_url='http://127.0.0.1:8000'):
        """
        Initiates a real PSTN voice phone call to mobile phone using Twilio REST API
        """
        config = TelephonyConfig.get_config()
        sid = config.twilio_account_sid
        auth_token = config.twilio_auth_token
        from_number = config.twilio_phone_number

        if not sid or not auth_token or not from_number:
            raise ValueError(
                "Twilio API credentials missing! Please click 'Telephony Keys' in the top navbar and enter your Twilio Account SID, Auth Token, and Twilio Phone Number."
            )

        # Twilio Calls REST Endpoint
        url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Calls.json"

        # Webhook URL for Twilio to fetch TwiML XML instructions when call is answered
        twiml_url = f"{host_url}/webhooks/twilio/start/?scenario_id={scenario.id}"

        data = {
            'To': phone_number,
            'From': from_number,
            'Url': twiml_url,
            'Method': 'POST'
        }

        response = requests.post(url, data=data, auth=(sid, auth_token), timeout=15)

        if response.status_code in [200, 201]:
            call_data = response.json()
            call_sid = call_data.get('sid', f"twilio-{scenario.id}")

            call_log = CallLog.objects.create(
                call_id=call_sid,
                scenario=scenario,
                title=scenario.title,
                category=scenario.category,
                recipient_name=scenario.recipient_name,
                phone_number=phone_number,
                engine_used='Twilio Real PSTN',
                status='In Progress',
                sentiment='Positive',
                extracted_data={'status': f'Real Call Dispatched to {phone_number}'}
            )

            CallTranscript.objects.create(
                call_log=call_log,
                speaker='AI',
                text=f"[Outgoing Call Dialing Mobile {phone_number}] {scenario.greeting}"
            )

            return call_log
        else:
            err_msg = response.json().get('message', response.text)
            raise ValueError(f"Twilio API Call Failed: {err_msg}")
