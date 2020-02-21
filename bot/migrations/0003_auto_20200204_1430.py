# Generated by Django 3.0.2 on 2020-02-04 12:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20200202_1304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegramuser',
            old_name='username',
            new_name='user_name',
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=300)),
                ('task_description', models.TextField()),
                ('task_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.TelegramUser')),
            ],
        ),
    ]
