from django.urls import path
from . import views

urlpatterns = [
    path('', views.machinesense_view, name='home'),
    path('machinesense/', views.machinesense_view, name='machinesense'),
    path('voice-dashboard/', views.dashboard_view, name='dashboard'),
    path('trigger-call/', views.trigger_call_view, name='trigger_call'),
    path('save-telephony-config/', views.save_telephony_config_view, name='save_telephony_config'),
    path('log/<int:log_id>/', views.log_detail_view, name='log_detail'),
    path('create-script/', views.create_script_view, name='create_script'),
    path('create-schedule/', views.create_schedule_view, name='create_schedule'),
    path('clear-logs/', views.clear_logs_view, name='clear_logs'),
    path('export/json/', views.export_logs_json, name='export_json'),
    path('export/csv/', views.export_logs_csv, name='export_csv'),
    path('webhooks/twilio/start/', views.twilio_start_webhook, name='webhooks_twilio_start'),
    path('webhooks/twilio/gather/', views.twilio_gather_webhook, name='webhooks_twilio_gather'),
    path('webhooks/retell/', views.webhooks_retell_view, name='webhooks_retell'),
    path('webhooks/vapi/', views.webhooks_vapi_view, name='webhooks_vapi'),
    path('machinesense/', views.machinesense_view, name='machinesense'),
]
