# Generated by Django 3.0.2 on 2020-02-02 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('user_password', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]