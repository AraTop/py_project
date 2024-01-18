from django.contrib import admin
from service.models import Settings, Message_to_Send, Mailing_Logs

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
   list_display = ('mailing_time_date', 'periodicity', 'mailing_status', 'client')

@admin.register(Message_to_Send)
class Message_to_SendAdmin(admin.ModelAdmin):
   list_display = ('letter_subject', 'letter_body', 'settings')

@admin.register(Mailing_Logs)
class Mailing_LogsAdmin(admin.ModelAdmin):
   list_display = ('date_and_time_of_last_attempt', 'attempt_status', 'mail_server_response', 'settings')