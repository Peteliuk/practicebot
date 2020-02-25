from django.db import models
from django.utils import timezone


""" TelegramUser Manager """


class TelegramUserQuerySet(models.QuerySet):
    def get_telegram_user(self, *args, **kwargs):
        return self.filter(*args, *kwargs).first()

    def set_telegram_user_telegram_id(self, user_id, telegram_id):
        self.filter(id=user_id).update(telegram_id=telegram_id)


class TelegramUserManager(models.Manager):
    def get_queryset(self):
        return TelegramUserQuerySet(self.model, using=self._db)

    def get_telegram_user(self, *args, **kwargs):
        return self.get_queryset().get_telegram_user(*args, **kwargs)

    def set_telegram_user_telegram_id(self, user_id, telegram_id):
        self.get_queryset().set_telegram_user_telegram_id(user_id, telegram_id)


""" Task Manager """


class TaskQuerySet(models.QuerySet):
    def get_all_tasks_ids_list(self, user_id):
        return [str(e.id) for e in self.filter(user_id=user_id).all()]

    def get_future_tasks(self, user_id):
        return self.filter(user_id=user_id, date__gt=timezone.now())

    def get_past_tasks(self, user_id):
        return self.filter(user_id=user_id, date__lte=timezone.now())

    def get_task(self, task_id):
        return self.get(id=task_id)

    def set_task_status(self, task_id, status):
        self.filter(id=task_id).update(status=status)


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def get_all_tasks_ids_list(self, user_id):
        return self.get_queryset().get_all_tasks_ids_list(user_id)

    def get_future_tasks(self, user_id):
        return self.get_queryset().get_future_tasks(user_id)

    def get_past_tasks(self, user_id):
        return self.get_queryset().get_past_tasks(user_id)

    def get_task(self, task_id):
        return self.get_queryset().get_task(task_id)

    def set_task_status(self, task_id, status):
        self.get_queryset().set_task_status(task_id, status)
