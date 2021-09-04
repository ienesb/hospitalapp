# Generated by Django 3.2.6 on 2021-09-04 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0035_alter_doctor_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='department',
            field=models.CharField(choices=[(1, 'Cardiologist'), (2, 'Dermatologists'), (3, 'Emergency Medicine Specialists'), (4, 'Allergists/Immunologists'), (5, 'Anesthesiologists'), (6, 'Colon and Rectal Surgeons')], max_length=50),
        ),
    ]
