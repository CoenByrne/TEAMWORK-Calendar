from flask import Flask, render_template
from src.TaskObjectBuilder import TaskObjectBuilder
from src.common.Database import Database
import src.TaskListHolder as List
from src.Tasks.Task import Task
from src.DatabaseChecker import DatabaseChecker

app = Flask(__name__)
app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    tasks = Task.get_tasks()
    return render_template("FullCalendar.html", tasks=tasks)


@app.route('/refresh')
def pull_data_from_api():
    TaskObjectBuilder.build_list(TaskObjectBuilder.get_from_teamwork())
    tsks = List.task_list
    for task in tsks:
        if not DatabaseChecker.does_task_exist_in_db(task):
            task.save_to_db()
        elif DatabaseChecker.has_task_been_updated(task):
            # write an update method
            task.update_in_db()
    tasks = Task.get_tasks()

    return render_template("FullCalendar.html", tasks=tasks)


app.run(debug=True, port=4992)



