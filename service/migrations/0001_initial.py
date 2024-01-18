# Generated by Django 4.2.9 on 2024-01-18 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_time_date', models.DateTimeField(verbose_name='Время рассылки')),
                ('periodicity', models.CharField(max_length=100, verbose_name='Периодичность')),
                ('mailing_status', models.CharField(max_length=100, verbose_name='Cтатус рассылки')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Настройка',
                'verbose_name_plural': 'Настройки',
                'ordering': ('mailing_time_date',),
            },
        ),
        migrations.CreateModel(
            name='Message_to_Send',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter_subject', models.CharField(max_length=200, verbose_name='Тема письма')),
                ('letter_body', models.TextField(verbose_name='Тело письма')),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_to_send', to='service.settings')),
            ],
            options={
                'verbose_name': 'Cообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ('letter_subject',),
            },
        ),
        migrations.CreateModel(
            name='Mailing_Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_and_time_of_last_attempt', models.DateTimeField(verbose_name='Дата и время последней попытки')),
                ('attempt_status', models.CharField(max_length=100, verbose_name='Статус попытки')),
                ('mail_server_response', models.TextField(max_length=100, verbose_name='Ответ почтового сервера')),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailing_logs', to='service.settings')),
            ],
            options={
                'verbose_name': 'Журнал рассылок',
                'verbose_name_plural': 'Журналы рассылок',
                'ordering': ('date_and_time_of_last_attempt',),
            },
        ),
    ]
