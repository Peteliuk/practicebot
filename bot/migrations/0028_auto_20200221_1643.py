# Generated by Django 3.0.2 on 2020-02-21 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0027_auto_20200221_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='telegram_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]
