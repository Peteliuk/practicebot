# Generated by Django 3.0.2 on 2020-02-15 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0018_auto_20200214_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskModule',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bot.Task')),
            ],
            bases=('bot.task',),
        ),
    ]
