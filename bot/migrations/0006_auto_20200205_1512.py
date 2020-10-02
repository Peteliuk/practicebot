# Generated by Django 3.0.2 on 2020-02-05 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20200205_0206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='task_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='task_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='telegramuser',
            old_name='user_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='telegramuser',
            old_name='user_password',
            new_name='password',
        ),
        migrations.AddField(
            model_name='task',
            name='acceed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='complited',
            field=models.BooleanField(default=False),
        ),
    ]
