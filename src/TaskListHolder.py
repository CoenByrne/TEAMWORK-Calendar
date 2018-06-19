# this task list holder will be used to run sorting methods and other things on the lists of tasks

task_list = []


def append_task(task):
    task_list.append(task)


def clear_task_list():
    task_list.clear()

# def sort_by_due_date():
#   for task in task_list:


def sort_list():
    arr_length = task_list.__len__()
    if arr_length > 1:
        for x in range(1, arr_length - 1, 1):
            if task_list[x-1].due_date < task_list[x].due_date:
                date_value = task_list[x].due_date
                priority_value = task_list[x].priority
                task = task_list[x]
                task_list[x] = task_list[x-1]
                for y in range(x, 0, -1):
                    if task_list[y].due_date < date_value:
                        task_list[y + 1] = task_list[y]
                    elif task_list[y].due_date > date_value:
                        task_list[y+1] = task
                    elif task_list[y].due_date == date_value & task_list[y].priority < priority_value:
                        task_list[y+1] = task_list[y]
                    elif task_list[y].due_date == date_value & task_list[y].priority > priority_value:
                        task_list[y+1] = task





