from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .models import TelegramUser
from .models import Task

class TelegramUserAdmin(admin.ModelAdmin):
	list_display = ('login', 'password', 'user_id')
	search_fields = ('login',)

class TaskAdmin(admin.ModelAdmin):
	list_display = ('name',	'date',	'user', 'acceed', 'complited')
	search_fields = ('name', 'user')

admin.site.site_header = 'Панель адміністратора'

admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Task, TaskAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
