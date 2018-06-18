from src.Tasks.Task import Task


class DatabaseChecker:

    @staticmethod
    def does_task_exist_in_db(task):
        tsk = Task.get_task(task["_id"])
        if tsk is None:
            return False
        else:
            return True

    @staticmethod
    def has_task_been_updated(task):
        tsk = Task.get_task(task["_id"])
        if task["last_changed_on"] == tsk["last_changed_on"]:
            return False
        else:
            return True


