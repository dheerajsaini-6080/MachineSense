from django import forms
from .models import CampaignScenario, TelephonyConfig

class TriggerCallForm(forms.Form):
    ENGINE_CHOICES = [
        ('twilio', '📞 Twilio Direct Mobile Call (Real PSTN Call to Phone)'),
        ('retell', '🤖 Retell AI Engine (Real Outbound Phone Call)'),
        ('vapi', '⚡ Vapi Voice AI (Real Outbound Phone Call)'),
        ('mock', '📱 Built-in Mobile Call Simulator (Demo Test)'),
    ]

    scenario_id = forms.IntegerField(widget=forms.HiddenInput())
    phone_number = forms.CharField(
        max_length=50,
        initial='+1 (555) 234-8901',
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono text-xs focus:outline-none focus:border-cyan-500',
            'placeholder': '+1 (555) 000-0000 or your mobile phone number'
        })
    )
    recipient_name = forms.CharField(
        max_length=150,
        initial='Alex Morgan',
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white text-xs focus:outline-none focus:border-cyan-500',
            'placeholder': 'Recipient Name'
        })
    )
    engine = forms.ChoiceField(
        choices=ENGINE_CHOICES,
        initial='twilio',
        widget=forms.Select(attrs={
            'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white text-xs focus:outline-none focus:border-cyan-500 cursor-pointer font-semibold'
        })
    )

class TelephonyConfigForm(forms.ModelForm):
    class Meta:
        model = TelephonyConfig
        fields = [
            'twilio_account_sid', 'twilio_auth_token', 'twilio_phone_number',
            'retell_api_key', 'retell_agent_id',
            'vapi_api_key', 'vapi_phone_number_id'
        ]
        widgets = {
            'twilio_account_sid': forms.TextInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white font-mono'}),
            'twilio_auth_token': forms.PasswordInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white font-mono', 'render_value': True}),
            'twilio_phone_number': forms.TextInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white font-mono', 'placeholder': '+1234567890'}),
            
            'retell_api_key': forms.PasswordInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white font-mono', 'render_value': True}),
            'retell_agent_id': forms.TextInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white font-mono'}),

            'vapi_api_key': forms.PasswordInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white font-mono', 'render_value': True}),
            'vapi_phone_number_id': forms.TextInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white font-mono'}),
        }

class CampaignForm(forms.ModelForm):
    class Meta:
        model = CampaignScenario
        fields = ['title', 'category', 'recipient_name', 'phone_number', 'description', 'greeting', 'closing_message']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white'}),
            'category': forms.TextInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white'}),
            'recipient_name': forms.TextInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white font-mono'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white'}),
            'greeting': forms.Textarea(attrs={'rows': 2, 'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white'}),
            'closing_message': forms.Textarea(attrs={'rows': 2, 'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white'}),
        }

class ScheduleForm(forms.Form):
    scenario_id = forms.IntegerField()
    phone_number = forms.CharField(max_length=50)
    delay_seconds = forms.IntegerField(initial=15)
