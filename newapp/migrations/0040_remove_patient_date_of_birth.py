# Generated by Django 3.2.7 on 2021-09-09 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0039_alter_patient_date_of_birth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='date_of_birth',
        ),
    ]
