# Generated by Django 3.0.3 on 2020-03-05 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0032_auto_20200303_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='telegram_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
