# Generated by Django 3.0.2 on 2020-02-06 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_auto_20200205_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='loginned',
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(default='No description'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='user_id',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
