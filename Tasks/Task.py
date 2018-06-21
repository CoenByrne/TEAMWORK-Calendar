from src.common.Database import Database
from src.Tasks.TaskConstants import COLLECTION


class Task(object):
    def __init__(self, task_id, start_date, due_date, description, content, project_name, project_id, todo_list_name,
                 creator_lastname, creator_firstname, estimated_minutes, has_dependencies, priority, progress,
                 last_changed_on, responsible_party_ids, responsible_party_id, responsible_party_names,
                 responsible_party_type, responsible_party_firstname, responsible_party_lastname,
                 responsible_party_summary):

        self.task_id = task_id
        self.start_date = start_date
        self.due_date = due_date
        self.description = description
        self.content = content
        self.project_name = project_name
        self.project_id = project_id
        self.todo_list_name = todo_list_name
        self.creator_lastname = creator_lastname
        self.creator_firstname = creator_firstname
        self.estimated_minutes = estimated_minutes
        self.has_dependencies = has_dependencies
        self.priority = priority
        self.progress = progress
        self.last_changed_on = last_changed_on
        self.responsible_party_ids = responsible_party_ids
        self.responsible_party_id = responsible_party_id
        self.responsible_party_names = responsible_party_names
        self.responsible_party_type = responsible_party_type
        self.responsible_party_firstname = responsible_party_firstname
        self.responsible_party_lastname = responsible_party_lastname
        self.responsible_party_summary = responsible_party_summary

    def json(self):
        return {
            "_id": int(self.task_id),
            "start_date": self.start_date,
            "due_date": self.due_date,
            "description": self.description,
            "content": self.content,
            "project_name": self.project_name,
            "project_id": self.project_id,
            "todo_list_name": self.todo_list_name,
            "creator_lastname": self.creator_lastname,
            "creator_firstname": self.creator_firstname,
            "estimated_minutes": self.estimated_minutes,
            "has_dependencies": self.has_dependencies,
            "priority": self.priority,
            "progress": self.progress,
            "last_changed_on": self.last_changed_on,
            "responsible_party_ids": self.responsible_party_ids,
            "responsible_party_id": self.responsible_party_id,
            "responsible_party_names": self.responsible_party_names,
            "responsible_party_type": self.responsible_party_type,
            "responsible_party_firstname": self.responsible_party_firstname,
            "responsible_party_lastname": self.responsible_party_lastname,
            "responsible_party_summary": self.responsible_party_summary
            }

    def save_to_db(self):
        Database.insert(COLLECTION, self.json())

    def update_in_db(self):
        Database.update(COLLECTION, {"_id": int(self.task_id)}, self.json())

    def delete_from_db(self):
        Database.remove(COLLECTION, {"_id": int(self.task_id)})

    @staticmethod
    def get_tasks():
        return Database.find(COLLECTION, {})

    @staticmethod
    def get_task(_id):
        return Database.find_one(COLLECTION, {"_id": int(_id)})

    @staticmethod
    def get_by_firstname_and_lastname(firstname, lastname):
        return Database.find(COLLECTION, {"creator_lastname": lastname, "creator_firstname": firstname})

    @staticmethod
    def get_placed_tasks():
        return Database.find("placed_tasks", {})  # this will be sorted by the responsible party and buissness (soon)

    @staticmethod
    def save_placed_task(task_json):
        Database.insert("placed_tasks", task_json)
