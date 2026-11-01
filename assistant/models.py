from django.db import models
import uuid

class TelephonyConfig(models.Model):
    twilio_account_sid = models.CharField(max_length=255, blank=True, default='')
    twilio_auth_token = models.CharField(max_length=255, blank=True, default='')
    twilio_phone_number = models.CharField(max_length=100, blank=True, default='', help_text="Your Twilio Purchased Phone Number (e.g. +1234567890)")
    
    retell_api_key = models.CharField(max_length=255, blank=True, default='')
    retell_agent_id = models.CharField(max_length=255, blank=True, default='')

    vapi_api_key = models.CharField(max_length=255, blank=True, default='')
    vapi_phone_number_id = models.CharField(max_length=255, blank=True, default='')

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Telephony API Configuration"

    @classmethod
    def get_config(cls):
        config, _ = cls.objects.get_or_create(id=1)
        return config

class CampaignScenario(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default='Custom')
    recipient_name = models.CharField(max_length=150, default='Client')
    phone_number = models.CharField(max_length=50, default='+1 (555) 000-0000')
    description = models.TextField(blank=True)
    badge_color = models.CharField(max_length=50, default='cyan')
    icon_name = models.CharField(max_length=50, default='FileText')
    greeting = models.TextField()
    closing_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

class CampaignQuestion(models.Model):
    scenario = models.ForeignKey(CampaignScenario, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    key = models.CharField(max_length=100)
    response_type = models.CharField(max_length=50, default='open_text')
    options = models.JSONField(default=list, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.scenario.title} - Q{self.order + 1}: {self.key}"

class CallLog(models.Model):
    call_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    scenario = models.ForeignKey(CampaignScenario, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default='General')
    recipient_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=50)
    engine_used = models.CharField(max_length=50, default='mock') # twilio, retell, vapi, mock
    timestamp = models.DateTimeField(auto_now_add=True)
    duration_seconds = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='Completed')
    sentiment = models.CharField(max_length=50, default='Positive')
    extracted_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Log {self.call_id} - {self.recipient_name} ({self.status})"

class CallTranscript(models.Model):
    call_log = models.ForeignKey(CallLog, on_delete=models.CASCADE, related_name='transcripts')
    speaker = models.CharField(max_length=20) # 'AI' or 'User'
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.speaker}: {self.text[:30]}"

class ScheduledCall(models.Model):
    scenario = models.ForeignKey(CampaignScenario, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=50)
    engine = models.CharField(max_length=50, default='mock')
    scheduled_time = models.DateTimeField()
    delay_seconds = models.IntegerField(default=30)
    status = models.CharField(max_length=50, default='Pending') # Pending, Triggered, Cancelled
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scheduled {self.scenario.title} for {self.recipient_name}"
