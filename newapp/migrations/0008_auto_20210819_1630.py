# Generated by Django 3.2.6 on 2021-08-19 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0007_delete_patientuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='last_name',
        ),
        migrations.AddField(
            model_name='patient',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='patient',
            name='password',
            field=models.CharField(default='ismail123', max_length=128),
        ),
    ]
