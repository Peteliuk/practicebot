# Generated by Django 3.0.2 on 2020-02-12 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0015_auto_20200210_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='tg_id',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
