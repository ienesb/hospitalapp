# Generated by Django 3.2.6 on 2021-08-19 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0008_auto_20210819_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
