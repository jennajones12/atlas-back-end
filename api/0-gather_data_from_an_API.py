#!/usr/bin/python3
"""
Returns to-do list information for a given employee ID.
"""
import json
import sys
import urllib.request

base_url = "https://jsonplaceholder.typicode.com/"

if __name__ == "__main__":

    if len(sys.argv) > 1:
        employee_id = int(sys.argv[1])
        url = base_url + "users/{}".format(employee_id)
        with urllib.request.urlopen(url) as response:
            user_data = response.read()
        user = json.loads(user_data)
        employee_name = user["name"]

        url = base_url + "todos?userId={}".format(employee_id)
        with urllib.request.urlopen(url) as response:
            todos_data = response.read()
            todos = json.loads(todos_data)

            completed = [todo["title"] for todo in todos if todo["completed"]]
        total_tasks = len(todos)
        completed_tasks_count = len(completed)

        print("Employee {} is done with tasks({}/{}):".format(
            employee_name, completed_tasks_count, total_tasks))

        for task in completed:
            print("\t {}".format(task))
    else:
        print("Please provide an employee ID as a command-line argument.")
