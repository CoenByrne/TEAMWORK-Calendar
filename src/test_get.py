import urllib3
from src.common import Utils

http = urllib3.PoolManager()

company = "wltc"
key = "twp_VJ8lmPZG8cdnAmW1UEYPqbHPzldj"
action = "tasks.json"

url = "https://{0}.teamwork.com/{1}".format(company, action)
headers = urllib3.util.make_headers(basic_auth=key + ":xxx")
request = http.request('GET', url, headers=headers)

response = request.status
data = request.data

dic = Utils.bytes_to_json(data)

tasks = dic["todo-items"]

for task in tasks:
    print(task)

    """
    What we need from each task
    - id
    - start-date
    - due-date
    - description
    - content
    - project-name
    - project-id (if we want to do put/post requests)
    - todo-list-name (task-list name)
    - creater-lastname
    - creater-firstname
    - start-date
    - estimated-minutes
    - has-dependencies
    - priority
    - progress
    """

    _id = task["id"]
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

    print(str(_id) + "\n" + str(start_date) + "\n" + str(due_date) + "\n" + str(description) + "\n" + str(content)
          + "\n" + str(project_name) + "\n" + str(project_id) + "\n" + str(todo_list_name) + "\n" +
          str(creator_lastname) + "\n" + str(creator_firstname) + "\n" + str(estimated_minutes) + "\n" +
          str(has_dependencies) + "\n" + str(priority) + "\n" + str(progress))

    """

    # task = Task(_id, start_date, due_date, description, content, project_name, project_id, task_list_name, 
    # creator_lastname, creator_firstname, estimated_minutes, has_dependencies, priority, progress)

    """





