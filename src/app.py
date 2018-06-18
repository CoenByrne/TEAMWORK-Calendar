from flask import Flask, render_template

from src.common.Database import Database
from src.TaskObjectBuilder import TaskListHolder
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


app.run(debug=True, port=4992)



