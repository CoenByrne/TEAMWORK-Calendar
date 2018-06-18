from src.common.Database import Database
from src.TaskObjectBuilder import TaskListHolder
from src.Tasks.Task import Task
from src.DatabaseChecker import DatabaseChecker

Database.initialize()

tasks = Task.get_tasks()
for task in tasks:
    print(DatabaseChecker.does_task_exist_in_db(task))
    print("- "*20)
    print(DatabaseChecker.has_task_been_updated(task))




