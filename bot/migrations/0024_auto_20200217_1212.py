# Generated by Django 3.0.2 on 2020-02-17 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0023_auto_20200217_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]
