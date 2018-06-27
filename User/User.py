from src.Tasks import TaskConstants
from src.common.Database import Database
from src.User import UserConstants


class User:

    def __init__(self, _id, user_name, password, company_id):
        self._id = _id
        self.user_name = user_name
        self.password = password
        self.company_id = company_id

    def json(self):
        return {
            "_id": int(self._id),
            "user_name": self.user_name,
            "password": self.password,
            "company_id": int(self.company_id)
        }

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def update_db(self):
        Database.update(UserConstants.COLLECTION, {"_id": self._id}, self.json())

    @staticmethod
    def from_db(user_name, password):
        return Database.find_one(UserConstants.COLLECTION, {"user_name": user_name, "password": password})

    @staticmethod
    def get_unplaced_user_tasks(company_id, user_id):
        return Database.find(TaskConstants.COLLECTION, {"responsible_party_id": user_id, "company_id": company_id})

    @staticmethod
    def get_placed_user_tasks(company_id, user_id):
        return Database.find(TaskConstants.placed_COLLECTION, {"responsible_party_id": user_id,
                                                               "company_id": company_id})

    @staticmethod
    def get_placed_anyone_tasks(company_id, user_id):
        return Database.find(TaskConstants.placed_COLLECTION, {"placed_by": user_id,
                                                               "company_id": company_id})

    @staticmethod
    def get_unplaced_tasks_anyone(company_id):
        return Database.find(TaskConstants.COLLECTION, {"company_id": company_id, "responsible_party_id": 0})

    @staticmethod
    def check_if_password_exists(user_id):
        user = Database.find_one(UserConstants.COLLECTION, {"_id": user_id})
        if user["password"] == "":
            return False
        else:
            return True

    @staticmethod
    def user_json_to_user_object(user_json):
        _id = user_json["_id"]
        user_name = user_json["user_name"]
        password = user_json["password"]
        company_id = user_json["company_id"]
        user = User(_id, user_name, password, company_id)
        return user