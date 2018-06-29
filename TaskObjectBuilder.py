import urllib3

from src.Tasks.PlacedTask import PlacedTask
from src.common import Utils
from src.Tasks.Task import Task
from src import TaskListHolder
from src.common.Database import Database


class TaskObjectBuilder:

    # this will eventually go into app
    Database.initialize()

    # need to write methods for scaling the program up, (support multiple company's) needs to be general.
    # key attached to buissness (set up the db to support it)
    @staticmethod
    def get_from_teamwork_scaled(actn, name, company_name, key):
        http = urllib3.PoolManager()
        company = company_name
        key = key
        action = actn

        url = "https://{0}.teamwork.com/{1}".format(company, action)
        headers = urllib3.util.make_headers(basic_auth=key + ":xxx")
        request = http.request('GET', url, headers=headers)

        data = request.data
        dic = Utils.bytes_to_json(data)
        tasks = dic[name]
        return tasks

    @staticmethod
    def build_list(tasks):
        for task in tasks:
            _id = task["id"]
            company_id = task["company-id"]
            start_date = task["start-date"]
            due_date = task["due-date"]
            description = task["description"]
            content = task["content"]
            project_name = task["project-name"]
            project_id = task["project-id"]
            todo_list_name = task["todo-list-name"]
            creator_lastname = task["creator-lastname"]
            creator_firstname = task["creator-firstname"]
            estimated_minutes = task["estimated-minutes"]
            has_dependencies = task["has-dependencies"]
            priority = task["priority"]
            progress = task["progress"]
            last_changed_on = task["last-changed-on"]
            if 'responsible-party-id' in task.keys():
                responsible_party_ids = task["responsible-party-ids"]
                responsible_party_id = task["responsible-party-id"]
                responsible_party_names = task["responsible-party-names"]
                responsible_party_type = task["responsible-party-type"]
                responsible_party_firstname = task["responsible-party-firstname"]
                responsible_party_lastname = task["responsible-party-lastname"]
                responsible_party_summary = task["responsible-party-summary"]

                tsk = Task(_id, company_id, start_date, due_date, description, content, project_name, project_id, todo_list_name,
                           creator_lastname, creator_firstname, estimated_minutes, has_dependencies, priority, progress,
                           last_changed_on, responsible_party_ids, responsible_party_id, responsible_party_names,
                           responsible_party_type, responsible_party_firstname, responsible_party_lastname,
                           responsible_party_summary)
                TaskListHolder.append_task(tsk)
                continue

            tsk = Task(_id, company_id, start_date, due_date, description, content, project_name, project_id, todo_list_name,
                       creator_lastname, creator_firstname, estimated_minutes, has_dependencies, priority, progress,
                       last_changed_on)

            TaskListHolder.append_task(tsk)
    # this is to be sent to a to the TaskListHolder
    # that class is to hold the sorting methods and contain an append_task() method to add a task to an ArrayList<Task>
    # append needs to be a static method.

    # TaskListHolder.append_task(tsk)

    @staticmethod
    def build_completed_list(tasks):
        for task in tasks:
            _id = task["id"]
            company_id = task["companyId"]
            start_date = task["startDate"]
            due_date = task["dueDate"]
            description = task["description"]
            content = task["content"]
            project_name = task["projectName"]
            project_id = task["projectId"]
            todo_list_name = ""
            creator_lastname = task["creatorLastName"]
            creator_firstname = ""
            estimated_minutes = ""
            has_dependencies = ""
            priority = ""
            progress = ""
            last_changed_on = ""
            responsible_party_ids = ""
            responsible_party_id = ""
            responsible_party_names = ""
            responsible_party_type = ""
            responsible_party_firstname = ""
            responsible_party_lastname = ""
            responsible_party_summary = ""

            tsk = Task(_id, company_id, start_date, due_date, description, content, project_name, project_id, todo_list_name,
                       creator_lastname, creator_firstname, estimated_minutes, has_dependencies, priority, progress,
                       last_changed_on, responsible_party_ids, responsible_party_id, responsible_party_names,
                       responsible_party_type, responsible_party_firstname, responsible_party_lastname,
                       responsible_party_summary)

            TaskListHolder.append_task(tsk)

    @staticmethod
    def build_placed_task_list(tasks):
        task_list = []
        for task in tasks:
            placed_task = TaskObjectBuilder.build_placed_task(task)
            task_list.append(placed_task)
        return task_list

    # method to turn an external task into a placed task
    @staticmethod
    def build_placed_task(task, start, end, placed_by_id):
        _id = task["_id"]
        company_id = task["company_id"]
        # variable to store the start time on the calender
        calender_start_time = start

        # variable to store the task end
        calender_end_time = end

        start_date = task["start_date"]
        due_date = task["due_date"]
        description = task["description"]
        content = task["content"]
        project_name = task["project_name"]
        project_id = task["project_id"]
        todo_list_name = task["todo_list_name"]
        creator_lastname = task["creator_lastname"]
        creator_firstname = task["creator_firstname"]
        estimated_minutes = task["estimated_minutes"]
        has_dependencies = task["has_dependencies"]
        priority = task["priority"]
        progress = task["progress"]
        last_changed_on = task["last_changed_on"]

        responsible_party_ids = task["responsible_party_ids"]
        responsible_party_id = task["responsible_party_id"]
        responsible_party_names = task["responsible_party_names"]
        responsible_party_type = task["responsible_party_type"]
        responsible_party_firstname = task["responsible_party_firstname"]
        responsible_party_lastname = task["responsible_party_lastname"]
        responsible_party_summary = task["responsible_party_summary"]
        placed_by = placed_by_id

        tsk = PlacedTask(_id, company_id, calender_start_time, calender_end_time, start_date, due_date, description,
                         content, project_name, project_id, todo_list_name, creator_lastname, creator_firstname,
                         estimated_minutes, has_dependencies, priority, progress, last_changed_on,
                         responsible_party_ids, responsible_party_id, responsible_party_names, responsible_party_type,
                         responsible_party_firstname, responsible_party_lastname, responsible_party_summary, placed_by)
        return tsk

    @staticmethod
    def build_task(task):
        _id = task["_id"]
        company_id = task["company_id"]
        start_date = task["start_date"]
        due_date = task["due_date"]
        description = task["description"]
        content = task["content"]
        project_name = task["project_name"]
        project_id = task["project_id"]
        todo_list_name = task["todo_list_name"]
        creator_lastname = task["creator_lastname"]
        creator_firstname = task["creator_firstname"]
        estimated_minutes = task["estimated_minutes"]
        has_dependencies = task["has_dependencies"]
        priority = task["priority"]
        progress = task["progress"]
        last_changed_on = task["last_changed_on"]

        responsible_party_ids = task["responsible_party_ids"]
        responsible_party_id = task["responsible_party_id"]
        responsible_party_names = task["responsible_party_names"]
        responsible_party_type = task["responsible_party_type"]
        responsible_party_firstname = task["responsible_party_firstname"]
        responsible_party_lastname = task["responsible_party_lastname"]
        responsible_party_summary = task["responsible_party_summary"]

        tsk = Task(_id, company_id, start_date, due_date, description, content, project_name, project_id, todo_list_name,
                   creator_lastname, creator_firstname, estimated_minutes, has_dependencies, priority, progress,
                   last_changed_on, responsible_party_ids, responsible_party_id, responsible_party_names,
                   responsible_party_type, responsible_party_firstname, responsible_party_lastname,
                   responsible_party_summary)

        return tsk
