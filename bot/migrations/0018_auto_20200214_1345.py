# Generated by Django 3.0.2 on 2020-02-14 11:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0017_auto_20200214_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
