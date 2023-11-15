import mysql.connector
from datetime import datetime

def generateTable():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kka"
    )

    list_tasks = {}

    temp = db.cursor()
    temp.execute("SELECT * FROM tasks")

    for index, row in enumerate(temp):
        task_info = {
            "taskName": row[0],
            "subject": row[1],
            "dl": None,
            "importance": row[3],
            "urgency": row[4]
        }

        deadline = row[2]
        curr_date = datetime.now().date()
        days_until_deadline = (deadline - curr_date).days
        task_info["dl"] = days_until_deadline

        list_tasks[index] = task_info

    temp.close()

    return list_tasks

list_tasks = generateTable()

for key, value in list_tasks.items():
    print(f"Task {key}: {value}")
