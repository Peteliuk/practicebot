from bot.models import Task


class TaskModule:
    """
    This is TaskModule class, what extends Task class.
    It provides you some functionality with `task` table in database.

    Methods:
        get_all_tasks_ids_list,
        get_future_tasks,
        get_last_tasks,
        get_task,
        set_task_status
    """

    @staticmethod
    def get_all_tasks_ids_list(user_id):
        """
        Gets all tasks ids list for some user

        :param user_id:     user's id in database
        return list of tasks ids
        """
        return Task.tasks.get_all_tasks_ids_list(user_id)

    @staticmethod
    def get_future_tasks(user_id):
        """
        Gets future tasks for some user

        :param user_id:     user's id
        return QuerySet object list of Task objects where date greater then today
        """
        return Task.tasks.get_future_tasks(user_id)

    @staticmethod
    def get_past_tasks(user_id):
        """
        Gets last tasks for some user

        :param user_id:     user's id
        return QuerySet object list of Task objects where date less then today and equals today
        """
        return Task.tasks.get_past_tasks(user_id)

    @staticmethod
    def get_task(task_id):
        """
        Gets task from database by its id

        :param task_id:     task's id
        return Task object
        """
        return Task.tasks.get_task(task_id)

    @staticmethod
    def set_task_status(task_id, status):
        """
        Sets status for some task

        :param task_id:     task's id
        :param status:      task's status (int)
        """
        Task.tasks.set_task_status(task_id, status)
