from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .models import TelegramUser
from .models import Task

from .services import TelegramUserService
from .services import TaskService


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'password', 'telegram_id', 'tasks_num')
    search_fields = ('email',)
    readonly_fields = ['password', 'telegram_id', 'tasks_num']

    @staticmethod
    def tasks_num(obj):
        return obj.task_set.count()

    def save_model(self, request, obj, form, change):
        TelegramUserService().create_telegram_user(obj)
        super().save_model(request, obj, form, change)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'user', 'status')
    search_fields = ('name', 'user')

    def save_model(self, request, obj, form, change):
        TaskService().notify_bot_about_task(obj)
        super().save_model(request, obj, form, change)


admin.site.site_header = 'Панель адміністратора'

admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Task, TaskAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
