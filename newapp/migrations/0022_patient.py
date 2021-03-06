# Generated by Django 3.2.6 on 2021-08-23 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('newapp', '0021_remove_appointment_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('first_name', models.CharField(default='PatientName', max_length=50)),
                ('last_name', models.CharField(default='PatientLastName', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
            ],
        ),
    ]
