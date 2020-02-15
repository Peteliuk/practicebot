from django.utils import timezone
from django.db.models import Q
from bot.models import Task


class TaskModule(Task):
    """
    This is TaskModule class, what extends Task class.
    It provides you some functionality with `task` table in database.

    Methods:
        get_all_tasks,
        get_future_tasks,
        get_last_tasks,
        get_task,
        set_task_status
    """

    def get_all_tasks(self, user_id):
        """
        Gets all tasks for some user

        :param user_id:     user's id
        return QuerySet object list of Task objects
        """
        return Task.objects.filter(user_id=user_id).all()

    def get_future_tasks(self, user_id):
        """
        Gets future tasks for some user

        :param user_id:     user's id
        return QuerySet object list of Task objects where date greater then today
        """
        return Task.objects.filter(Q(user_id=user_id) & Q(date__gt=timezone.now()))

    def get_past_tasks(self, user_id):
        """
        Gets last tasks for some user

        :param user_id:     user's id
        return QuerySet object list of Task objects where date less then today and equals today
        """
        return Task.objects.filter(Q(user_id=user_id) & Q(date__lte=timezone.now()))

    def get_task(self, task_id):
        """
        Gets task from database by its id

        :param task_id:     task's id
        return Task object
        """
        return Task.objects.get(id=task_id)

    def set_task_status(self, task_id, status):
        """
        Sets status for some task

        :param task_id:     task's id
        :param status:      task's status (int)
        """
        task = Task.objects.get(id=task_id)
        task.status = status
        task.save()
