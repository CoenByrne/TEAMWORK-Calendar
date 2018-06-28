from src.common.Database import Database


class PlacedTask(object):
    def __init__(self, task_id, company_id, calender_start_time, start_date, due_date, description, content, project_name, project_id, todo_list_name,
                 creator_lastname, creator_firstname, estimated_minutes, has_dependencies, priority, progress,
                 last_changed_on, responsible_party_ids, responsible_party_id, responsible_party_names,
                 responsible_party_type, responsible_party_firstname, responsible_party_lastname,
                 responsible_party_summary, placed_by):

        self.task_id = task_id
        self.company_id = company_id
        self.calender_start_time = calender_start_time
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
        self.placed_by = placed_by

    def json(self):
        return {
            "_id": int(self.task_id),
            "company_id": self.company_id,
            "start": self.calender_start_time,
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
            "responsible_party_id": int(self.responsible_party_id),
            "responsible_party_names": self.responsible_party_names,
            "responsible_party_type": self.responsible_party_type,
            "responsible_party_firstname": self.responsible_party_firstname,
            "responsible_party_lastname": self.responsible_party_lastname,
            "responsible_party_summary": self.responsible_party_summary,
            "placed_by": self.placed_by
            }

    def update_task(self):
        Database.update("placed_tasks", {"_id": self.task_id}, self.json())

    def save_placed_task(self):
        Database.insert("placed_tasks", self.json())

    # add a query for current user pass variable in through method.
    # also need one for current business
    @staticmethod
    def get_placed_tasks():
        return Database.find("placed_tasks", {})  # this will be sorted by the responsible party and buissness (soon)

    @staticmethod
    def get_task(_id):
        return Database.find_one("placed_tasks", {"_id": int(_id)})

    @staticmethod
    def remove_placed_task(task_id):
        Database.remove("placed_tasks", {"_id": int(task_id)})
