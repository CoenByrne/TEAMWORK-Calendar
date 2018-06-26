import json
from flask import Flask, render_template, request, jsonify
from bson import json_util

from src.Company import CompanyConstants
from src.Company.Company import Company
from src.TaskObjectBuilder import TaskObjectBuilder
from src.Tasks.PlacedTask import PlacedTask
from src.User import UserConstants
from src.common.Database import Database
import src.TaskListHolder as List
from src.Tasks.Task import Task
from src.Tasks import TaskConstants as T
from src.DatabaseChecker import DatabaseChecker
from src.common import Utils

app = Flask(__name__)
app.secret_key = "123"


# the only method that should not change ever.
@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/companyLogin', methods=['GET', 'POST'])
def company_login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        company_name = request.form['name']
        company_password = request.form['password']
        if Company.login_company(company_name, company_password):
            company = Database.find_one(CompanyConstants.COLLECTION, {"company_name": company_name})
            print(company)
            users = Database.find(UserConstants.COLLECTION, {"company_id": str(company["_id"])})
            user_names = []
            for user_id in users:

                print(user_id)
                user_names.append(user_id["user_name"])
            print(user_names)
            return render_template("userPicker.html", user_names=user_names)
        else:
            return render_template("home.html", string="please use a valid login")


@app.route('/companyRegister', methods=['GET', 'POST'])
def company_register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        company_name = request.form['name']
        company_password = request.form['password']
        company_teamwork_key = request.form['key']

        string = Company.register_company(company_name, company_password, company_teamwork_key)

        return render_template("home.html", string=string)


# landing-page/login needs to be loaded before loading up the calender to allow session["company"] and session["user"]
# to be filled in before reaching the calender.
@app.route('/calendar')
def calendar():
    tasks = Task.get_tasks()
    if tasks is None:
        pull_from_teamwork()
        tasks = Task.get_tasks()
        if tasks is None:
            return render_template("FullCalendar.html")
    return render_template("FullCalendar.html", tasks=tasks)


# needs to be more general, eg. allowing pulling data from different companies. (this means editing the Task
# class db queries)
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

    tasks = Task.get_tasks()
    return render_template("FullCalendar.html", tasks=tasks)


# name needs changing, also method needs to be changed to support multiple company's/users as well as assigning the
# current user the task unless its a multi-user task
@app.route('/retrieve_data', methods=["POST"])
def post_request():
    if request.method == "POST":
        event_data = request.get_data('data')
        event_json = Utils.bytes_to_json(event_data)
        TaskObjectBuilder.build_placed_task(Task.get_task(event_json["id"]), event_json["start"]).save_placed_task()
        Task.remove_task(event_json["id"])
        # add to db.placed_tasks here
        # delete from db.External_tasks using the id
        return render_template("FullCalendar.html")


# the name of this method needs to be changed to get_external_events
# this needs to be scaled up to support only getting data relevant to the current user
@app.route('/external')
def get_request():
    mongo_dic = Task.get_tasks()
    dic = {"data": []}
    for task in mongo_dic:
        dic["data"].append(json_util.dumps(task))
    return jsonify(dic)


# get by company & user (include tasks for anyone)
@app.route('/placed')
def get_placed_tasks():
    mongo_dic = PlacedTask.get_placed_tasks()
    dic = {"data": []}
    for task in mongo_dic:
        dic["data"].append(json_util.dumps(task))
    return jsonify(dic)


# remove user assigned to task (if not a multiUser task)
@app.route('/post_back_to_external_events', methods=["POST"])
def post_back_to_external_events():
    if request.method == "POST":
        event_data = request.get_data('data')
        event_json = Utils.bytes_to_json(event_data)
        TaskObjectBuilder.build_task(PlacedTask.get_task(event_json["id"])).save_to_db()
        PlacedTask.remove_placed_task(event_json["id"])
        return render_template("FullCalendar.html")


# add functionality to pull data from more then one company's TEAMWORK site.
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


app.run(debug=True, port=4992)


