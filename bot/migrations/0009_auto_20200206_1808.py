# Generated by Django 3.0.2 on 2020-02-06 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_auto_20200206_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='login',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='user_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
