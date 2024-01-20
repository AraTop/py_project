from django.core.mail import send_mail
import pytz
from project import settings
from service.models import Mailing_Logs, Message_to_Send, Settings
from django.utils import timezone
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from celery import shared_task
from datetime import datetime, timedelta


@shared_task
def send_mailing_task(mailing, message, current_date_time, recipient):
   subject = mailing.letter_subject
   message = mailing.letter_body

   try:
      send_mail(
         subject=subject,
         message=message,
         from_email=settings.EMAIL_HOST_USER,
         recipient_list=[recipient.email])
         
      log = Mailing_Logs(
         date_and_time_of_last_attempt=current_date_time,
         attempt_status="Success",
         mail_server_response="Success",
         settings=Settings.objects.filter(client_id=recipient.pk))
      log.save()

   except Exception as e:
      log = Mailing_Logs(
         date_and_time_of_last_attempt=current_date_time,
         attempt_status="Error",
         mail_server_response=e,
         settings=Settings.objects.filter(client_id=recipient.pk))
      log.save()

   mailing.save()

@shared_task
def start_mailings():
   """
   Функция для запуска отложенных рассылок.
   Эта функция будет вызываться периодически по расписанию и отправлять рассылки,
   которые готовы к отправке на текущий момент.
   Периодичность отправки рассылок зависит от настроек каждой рассылки.
   """
   
   zone = pytz.timezone(settings.TIME_ZONE)
   current_date_time = datetime.now(zone)

   mailings = Settings.objects.filter(mailing_time_date__lte=current_date_time)

   for mailing in mailings:

      message = Message_to_Send.objects.get(settings=mailing)
      recipient = mailing.client
      print(recipient)
      send_mailing_task.delay(mailing, message, current_date_time, recipient)

      if mailing.periodicity == "раз в день":
         mailing.mailing_time_date += timedelta(days=1)
      elif mailing.periodicity == "раз в неделю":
         mailing.mailing_time_date += timedelta(weeks=1)
      elif mailing.periodicity == "раз в месяц":
         mailing.mailing_time_date += relativedelta(months=1)

      if mailing.mailing_time_date.day > 28:
         mailing.mailing_time_date = mailing.mailing_time_date.replace(day=1)
         mailing.mailing_time_date += relativedelta(day=31)

      mailing.save()
