from src.Tasks.PlacedTask import PlacedTask
from src.Tasks.Task import Task


class DatabaseChecker:

    @staticmethod
    def does_task_exist_in_db(task):
        tsk = Task.get_task(task.task_id)
        if tsk is None:
            return False
        else:
            return True

    @staticmethod
    def has_task_been_updated(task):
        tsk = Task.get_task(task.task_id)
        if task.last_changed_on == tsk["last_changed_on"]:
            return False
        else:
            return True

    @staticmethod
    def does_placed_task_exist_in_db(task):
        tsk = PlacedTask.get_task(task.task_id)
        if tsk is None:
            return False
        else:
            return True
