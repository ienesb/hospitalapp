# Generated by Django 3.2.7 on 2021-09-07 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0037_auto_20210906_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='department',
            field=models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Dermatologists', 'Dermatologists'), ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'), ('Allergists/Immunologists', 'Allergists/Immunologists'), ('Anesthesiologists', 'Anesthesiologists'), ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')], max_length=50),
        ),
    ]
