from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .models import TelegramUser
from .models import Task


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('login', 'password', 'tg_id', 'tasks_num')
    search_fields = ('login',)
    readonly_fields = ['tg_id', 'tasks_num']

    def tasks_num(self, obj):
        return obj.task_set.count()


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'user', 'status')
    search_fields = ('name', 'user')


admin.site.site_header = 'Панель адміністратора'

admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Task, TaskAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
