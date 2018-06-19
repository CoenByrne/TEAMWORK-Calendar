from flask import Flask, render_template
from src.TaskObjectBuilder import TaskObjectBuilder
from src.common.Database import Database
import src.TaskListHolder as List
from src.Tasks.Task import Task
from src.Tasks import TaskConstants as T
from src.DatabaseChecker import DatabaseChecker
from src.common import Utils

app = Flask(__name__)
app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    tasks = Task.get_tasks()
    if tasks is None:
        pull_from_teamwork()
        tasks = Task.get_tasks()
        if tasks is None:
            return render_template("FullCalendar.html")
    return render_template("FullCalendar.html", tasks=tasks)


@app.route('/refresh')
def pull_data_from_api():
    pull_from_teamwork()

    List.clear_task_list()
    TaskObjectBuilder.build_completed_list(TaskObjectBuilder.get_from_teamwork(T.completed_tasks, T.completed_tasks_name))
    ts = List.task_list
    for task in ts:
        print(DatabaseChecker.does_task_exist_in_db(task))
        print(task.task_id)
        if DatabaseChecker.does_task_exist_in_db(task):
            task.delete_from_db()

    tasks = Task.get_tasks()
    return render_template("FullCalendar.html", tasks=tasks)


def pull_from_teamwork():
    List.clear_task_list()
    TaskObjectBuilder.build_list(TaskObjectBuilder.get_from_teamwork(T.tasks, T.tasks_name))
    tsks = List.task_list
    for task in tsks:
        if not DatabaseChecker.does_task_exist_in_db(task):
            task.save_to_db()
        elif DatabaseChecker.has_task_been_updated(task):
            # write an update method
            task.update_in_db()
        # elif DatabaseChecker.



app.run(debug=True, port=4992)



