from src.Company import CompanyConstants
from src.TaskObjectBuilder import TaskObjectBuilder
from src.User import UserConstants
from src.User.User import User
from src.common import Utils
from src.common.Database import Database
from src.Company.CompanyConstants import COLLECTION


class Company:

    def __init__(self, _id, company_name, password, key, users):
        self._id = _id
        self.company_name = company_name
        self.password = password
        self.key = key
        self.users = users

    def save_to_db(self):
        Database.insert(COLLECTION, self.json())

    def json(self):
        return {
            "_id": int(self._id),
            "key": self.key,
            "company_name": self.company_name,
            "password": self.password,
            "users": self.users
        }

    @staticmethod
    def from_db(company_name):
        return Database.find_one(COLLECTION, {"company_name": company_name})

    @staticmethod
    def create_user_id_list(company_name, company_key):
        people = TaskObjectBuilder.get_from_teamwork_scaled(CompanyConstants.people_action,
                                                            CompanyConstants.people_name,
                                                            company_name, company_key)
        user_ids = []
        for person in people:
            user_name = person["user-name"]
            _id = person["id"]
            pin = ""

            # user = User(_id, user_name, pin, company_id)
            user_ids.append(_id)
        return user_ids

    @staticmethod
    def get_users_from_db(company_id):
        return Database.find(UserConstants.COLLECTION, {"company_id": company_id})

    @staticmethod
    def register_company(company_name, company_password, key):
        company_data = Database.find_one(COLLECTION, {"company_name": company_name, "key": key})

        # needs to catch JSON decoder error and return invalid company name and key
        account = TaskObjectBuilder.get_from_teamwork_scaled(CompanyConstants.account_action,
                                                             CompanyConstants.account_name,
                                                             company_name, key)
        people = Company.create_user_id_list(company_name, key)
        if company_data is not None:
            return "already registered"

        elif "companyid" in account.keys():
            _id = account["companyid"]
            company = Company(_id, company_name, Utils.hash_password(company_password), key, people)
            company.save_to_db()
            return "company registered"
        else:
            return "invalid company name or API key"

    @staticmethod
    def login_company(company_name, password):
        company_data = Database.find_one(COLLECTION, {"company_name": company_name})
        if company_data is None:
            return False
        if Utils.check_hashed_password(password, company_data['password']):
            return True
        else:
            return False


