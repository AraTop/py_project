from django.db import models
from users.models import User

NULLABLE = {'null':True, 'blank':True}

class Settings(models.Model):
    mailing_time_date = models.DateTimeField(verbose_name='Время рассылки')
    periodicity = models.CharField(max_length=100, verbose_name='Периодичность')
    mailing_status = models.CharField(max_length=100, verbose_name='Cтатус рассылки')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settings')
   
    def __str__(self):
        return f'{self.mailing_time_date} {self.periodicity} {self.mailing_status}' 
   
    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
        ordering = ('mailing_time_date',)

class Message_to_Send(models.Model):
    letter_subject = models.CharField(max_length=200, verbose_name='Тема письма')
    letter_body = models.TextField(verbose_name='Тело письма')
    settings = models.ForeignKey(Settings, on_delete=models.CASCADE, related_name='message_to_send')
   
    def __str__(self):
        return f'{self.letter_subject} {self.letter_body} {self.settings}' 
   
    class Meta:
        verbose_name = 'Cообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('letter_subject',)

class Mailing_Logs(models.Model):
    date_and_time_of_last_attempt = models.DateTimeField(verbose_name='Дата и время последней попытки')
    attempt_status = models.CharField(max_length=100, verbose_name='Статус попытки')
    mail_server_response = models.TextField(max_length=100, verbose_name='Ответ почтового сервера')
    settings = models.ForeignKey(Settings, on_delete=models.CASCADE, related_name='mailing_logs')
   
    def __str__(self):
        return f'{self.date_and_time_of_last_attempt} {self.attempt_status} {self.settings}' 
   
    class Meta:
        verbose_name = 'Журнал рассылок'
        verbose_name_plural = 'Журналы рассылок'
        ordering = ('date_and_time_of_last_attempt',)