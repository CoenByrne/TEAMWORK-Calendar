import json
from flask import Flask, render_template, request, jsonify, session
from bson import json_util

from src.Company import CompanyConstants
from src.Company.Company import Company
from src.TaskObjectBuilder import TaskObjectBuilder
from src.Tasks.PlacedTask import PlacedTask
from src.User import UserConstants
from src.User.User import User
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

            # give the company_id to the session to access later on
            session["company_id"] = company["_id"]
            session["company_name"] = company_name
            Company.update_users(company_name, company["key"], session["company_id"])
            users = Database.find(UserConstants.COLLECTION, {"company_id": company["_id"]})
            user_names = []
            for user_id in users:
                user_names.append(user_id["user_name"])
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


@app.route('/pickUser', methods=["POST"])
def pick_user():
    if request.method == 'POST':
        user_name = request.form.get("pick_user")
        user = Database.find_one(UserConstants.COLLECTION, {"user_name": user_name})
        user_id = user["_id"]
        session["user_name"] = user_name
        session["user_id"] = user_id
        User.get_unplaced_tasks_anyone(session["company_id"])
        User.get_placed_user_tasks(session["company_id"], user_id)
        User.get_unplaced_user_tasks(session["company_id"], user_id)
        if user["password"] == "":
            return render_template("createPassword.html")
        return render_template("userLogin.html")
# landing-page/login needs to be loaded before loading up the calender to allow session["company"] and session["user"]
# to be filled in before reaching the calender.


@app.route('/createPassword', methods=["POST"])
def create_password():
    if request.method == 'POST':
        password = request.form['password']
        password_second = request.form['password_repeated']
        if password == password_second:
            hashed_password = Utils.hash_password(password)
            user = Database.find_one(UserConstants.COLLECTION, {"_id": session["user_id"]})
            user["password"] = hashed_password
            # update user in db
            User.user_json_to_user_object(user).update_db()
            return render_template("FullCalendar.html")
        else:
            error_message = "passwords don't match, please re-enter them"
            return render_template('createPassword.html', error_message=error_message)


@app.route('/enter_password', methods=["POST"])
def enter_password():
    if request.method == 'POST':
        password = request.form["password"]
        user_data = Database.find_one(UserConstants.COLLECTION, {"_id": session["user_id"]})
        if user_data is not None:
            if Utils.check_hashed_password(password, user_data['password']):
                return render_template('FullCalendar.html')
            else:
                return render_template('userLogin.html', error_message="please enter the correct password")
        else:
            return render_template("home.html", string="something went wrong please try again")


@app.route('/calendar')
def calendar():
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
    company = Database.find_one(CompanyConstants.COLLECTION, {"_id": session["company_id"]})
    List.clear_task_list()
    TaskObjectBuilder.build_completed_list(TaskObjectBuilder.get_from_teamwork_scaled(T.completed_tasks,
                                                                                      T.completed_tasks_name,
                                                                                      session["company_name"],
                                                                                      company["key"]))
    ts = List.task_list
    for task in ts:
        if DatabaseChecker.does_task_exist_in_db(task):
            task.delete_from_db()
        elif DatabaseChecker.does_placed_task_exist_in_db(task):
            PlacedTask.remove_placed_task(task.task_id)
    return render_template("FullCalendar.html")


# ----------------- these methods are specific to calendar ---------------

@app.route('/retrieve_data', methods=["POST"])
def post_request():
    if request.method == "POST":
        event_data = request.get_data('data')
        event_json = Utils.bytes_to_json(event_data)
        task = TaskObjectBuilder.build_placed_task(Task.get_task(event_json["id"]), event_json["start"],
                                                   event_json["end"], session["user_id"])
        task.save_placed_task()
        Task.remove_task(event_json["id"])
        # add to db.placed_tasks here
        # delete from db.External_tasks using the id
        return render_template("FullCalendar.html")


@app.route('/update_task', methods=["POST"])
def update_task():
    if request.method == "POST":
        event_data = request.get_data('data')
        event_json = Utils.bytes_to_json(event_data)
        print(event_json)
        task = TaskObjectBuilder.build_placed_task(PlacedTask.get_task(event_json["id"]), event_json["start"],
                                                   event_json["end"], session["user_id"])
        task.update_task()
        return render_template("FullCalendar.html")


@app.route('/external')
def get_request():
    mongo_dic = User.get_unplaced_user_tasks(session["company_id"], session["user_id"])
    dic = {"data": []}
    for task in mongo_dic:
        dic["data"].append(json_util.dumps(task))
    mongo_dic_anyone = User.get_unplaced_tasks_anyone(session["company_id"])
    for task in mongo_dic_anyone:
        dic["data"].append(json_util.dumps(task))
    return jsonify(dic)


# get by company & user (include tasks for anyone)
@app.route('/placed')
def get_placed_tasks():
    mongo_dic = User.get_placed_user_tasks(session["company_id"], session["user_id"])

    dic = {"data": []}
    for task in mongo_dic:
        dic["data"].append(json_util.dumps(task))
    mongo_dic_anyone = User.get_placed_anyone_tasks(session["company_id"], session["user_id"])
    for task in mongo_dic_anyone:
        if task["placed_by"] == session["user_id"] and task["responsible_party_id"] == 0:
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


