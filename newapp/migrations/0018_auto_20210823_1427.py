# Generated by Django 3.2.6 on 2021-08-23 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0017_auto_20210823_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.doctor'),
        ),
        migrations.AlterField(
            model_name='record',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.doctor'),
        ),
    ]
