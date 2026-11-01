from django.contrib import admin
from .models import CampaignScenario, CampaignQuestion, CallLog, CallTranscript, ScheduledCall

class CampaignQuestionInline(admin.TabularInline):
    model = CampaignQuestion
    extra = 1

@admin.register(CampaignScenario)
class CampaignScenarioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'recipient_name', 'phone_number', 'created_at')
    search_fields = ('title', 'category', 'recipient_name')
    inlines = [CampaignQuestionInline]

class CallTranscriptInline(admin.TabularInline):
    model = CallTranscript
    extra = 0
    readonly_fields = ('speaker', 'text', 'timestamp')

@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):
    list_display = ('call_id', 'title', 'recipient_name', 'phone_number', 'engine_used', 'status', 'sentiment', 'duration_seconds', 'timestamp')
    list_filter = ('category', 'status', 'sentiment', 'engine_used')
    search_fields = ('title', 'recipient_name', 'phone_number', 'call_id')
    inlines = [CallTranscriptInline]

@admin.register(ScheduledCall)
class ScheduledCallAdmin(admin.ModelAdmin):
    list_display = ('scenario', 'recipient_name', 'phone_number', 'engine', 'scheduled_time', 'status')
    list_filter = ('status', 'engine')
