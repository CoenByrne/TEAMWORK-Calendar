import json
from flask import Flask, render_template, request, jsonify
from bson import json_util

from src.TaskObjectBuilder import TaskObjectBuilder
from src.Tasks.PlacedTask import PlacedTask
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
        if DatabaseChecker.does_task_exist_in_db(task):
            task.delete_from_db()
        elif DatabaseChecker.does_placed_task_exist_in_db(task):
            PlacedTask.remove_placed_task(task.task_id)
        else:
            tasks = Task.get_tasks()

    return render_template("FullCalendar.html", tasks=tasks)


@app.route('/retrieve_data', methods=["POST"])
def post_request():
    if request.method == "POST":
        event_data = request.get_data('data')
        event_json = Utils.bytes_to_json(event_data)
        print(event_json["start"])
        TaskObjectBuilder.build_placed_task(Task.get_task(event_json["id"]), event_json["start"]).save_placed_task()
        Task.remove_task(event_json["id"])
        # add to db.placed_tasks here
        # delete from db.External_tasks using the id
        return render_template("FullCalendar.html")


@app.route('/external')
def get_request():
    mongo_dic = Task.get_tasks()
    dic = {"data": []}
    for task in mongo_dic:
        dic["data"].append(json_util.dumps(task))
    return jsonify(dic)


def pull_from_teamwork():
    List.clear_task_list()
    TaskObjectBuilder.build_list(TaskObjectBuilder.get_from_teamwork(T.tasks, T.tasks_name))
    tsks = List.task_list
    for task in tsks:
        if not DatabaseChecker.does_task_exist_in_db(task):
            if not DatabaseChecker.does_placed_task_exist_in_db(task):
                task.save_to_db()
        elif DatabaseChecker.has_task_been_updated(task):
            # write an update method
            task.update_in_db()
        # elif DatabaseChecker.


@app.route('/placed')
def get_placed_tasks():
    mongo_dic = PlacedTask.get_placed_tasks()
    dic = {"data": []}
    for task in mongo_dic:
        dic["data"].append(json_util.dumps(task))
    return jsonify(dic)


app.run(debug=True, port=4992)


