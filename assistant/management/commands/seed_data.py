from django.core.management.base import BaseCommand
from assistant.models import CampaignScenario, CampaignQuestion, CallLog, CallTranscript
import random

class Command(BaseCommand):
    help = 'Seeds initial campaign scenarios and call logs into SQLite DB'

    def handle(self, *args, **options):
        self.stdout.write('Seeding initial Django database models...')

        # 1. Medication & Health Check
        sc1, _ = CampaignScenario.objects.get_or_create(
            title='Daily Medication & Health Check',
            defaults={
                'category': 'Healthcare',
                'recipient_name': 'Alex Morgan',
                'phone_number': '+1 (555) 234-8901',
                'description': 'Verifies daily medication compliance and collects wellness rating & symptom updates.',
                'badge_color': 'emerald',
                'icon_name': 'HeartPulse',
                'greeting': 'Hello Alex! This is your EchoCall Health Assistant checking in for your daily wellness update.',
                'closing_message': 'Thank you for updating your health log, Alex! Have a fantastic day ahead. Goodbye!'
            }
        )
        if not sc1.questions.exists():
            CampaignQuestion.objects.create(scenario=sc1, text='Did you take your prescribed morning medication today?', key='medication_taken', response_type='yes_no', options=['Yes', 'No'], order=0)
            CampaignQuestion.objects.create(scenario=sc1, text='On a scale of 1 to 5, how are you feeling overall right now?', key='wellness_rating', response_type='rating', options=['1', '2', '3', '4', '5'], order=1)
            CampaignQuestion.objects.create(scenario=sc1, text='Are you experiencing any unusual symptoms or side effects today?', key='symptoms_reported', response_type='open_text', order=2)

        # 2. Dental Appointment Confirmation
        sc2, _ = CampaignScenario.objects.get_or_create(
            title='Appointment Confirmation & Reminder',
            defaults={
                'category': 'Reminders',
                'recipient_name': 'Jordan Lee',
                'phone_number': '+1 (555) 789-4321',
                'description': 'Confirms attendance for upcoming dental checkup and arranges SMS alerts.',
                'badge_color': 'cyan',
                'icon_name': 'CalendarCheck',
                'greeting': 'Hi Jordan! Calling from CityCare Dental to confirm your upcoming appointment tomorrow at 10:00 AM.',
                'closing_message': 'Wonderful! Your appointment status has been updated in our system. See you tomorrow!'
            }
        )
        if not sc2.questions.exists():
            CampaignQuestion.objects.create(scenario=sc2, text='Can you confirm if you will be attending your scheduled appointment tomorrow at 10:00 AM?', key='appointment_confirmed', response_type='confirmation', options=['Confirm', 'Reschedule', 'Cancel'], order=0)
            CampaignQuestion.objects.create(scenario=sc2, text='Would you like us to send an automated SMS reminder with directions 1 hour before?', key='sms_alert_requested', response_type='yes_no', options=['Yes', 'No'], order=1)

        # 3. Post-Delivery Satisfaction Survey
        sc3, _ = CampaignScenario.objects.get_or_create(
            title='Post-Delivery Satisfaction Survey',
            defaults={
                'category': 'Feedback',
                'recipient_name': 'Taylor Swift',
                'phone_number': '+1 (555) 345-6789',
                'description': 'Collects quick customer rating and open feedback following a recent product delivery.',
                'badge_color': 'purple',
                'icon_name': 'Star',
                'greeting': 'Hello Taylor! Thanks for choosing Apex Express. We have a 20-second feedback check on your recent package delivery.',
                'closing_message': 'We truly appreciate your feedback! Your insights help us improve every day. Thank you!'
            }
        )
        if not sc3.questions.exists():
            CampaignQuestion.objects.create(scenario=sc3, text='How satisfied were you with the speed and condition of your delivery on a scale of 1 to 5?', key='satisfaction_score', response_type='rating', options=['1', '2', '3', '4', '5'], order=0)
            CampaignQuestion.objects.create(scenario=sc3, text='Is there any comment or suggestion you would like to share with our support team?', key='feedback_comment', response_type='open_text', order=1)

        # Seed sample CallLogs if DB is empty
        if not CallLog.objects.exists():
            log1 = CallLog.objects.create(
                call_id='log-101',
                scenario=sc1,
                title=sc1.title,
                category=sc1.category,
                recipient_name=sc1.recipient_name,
                phone_number=sc1.phone_number,
                engine_used='Retell AI',
                duration_seconds=42,
                status='Completed',
                sentiment='Positive',
                extracted_data={'medication_taken': 'Yes', 'wellness_rating': '5/5', 'symptoms_reported': 'Feeling energetic, no side effects.'}
            )
            CallTranscript.objects.create(call_log=log1, speaker='AI', text=sc1.greeting)
            CallTranscript.objects.create(call_log=log1, speaker='AI', text='Did you take your prescribed morning medication today?')
            CallTranscript.objects.create(call_log=log1, speaker='User', text='Yes, I took it right after breakfast.')
            CallTranscript.objects.create(call_log=log1, speaker='AI', text='On a scale of 1 to 5, how are you feeling overall right now?')
            CallTranscript.objects.create(call_log=log1, speaker='User', text='I feel great, 5 out of 5!')
            CallTranscript.objects.create(call_log=log1, speaker='AI', text=sc1.closing_message)

        self.stdout.write(self.style.SUCCESS('Successfully seeded Django database!'))
