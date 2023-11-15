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
        task_info = [
            row[0],  # taskName
            row[1],  # subject
            None,    # dl (to be calculated later)
            row[3],  # importance
            row[4]   # urgency
        ]

        deadline = row[2]
        curr_date = datetime.now().date()
        days_until_deadline = (deadline - curr_date).days
        task_info[2] = days_until_deadline  # set the dl value

        list_tasks[index] = task_info

    temp.close()

    return list_tasks

list_tasks = generateTable()

for key, value in list_tasks.items():
    print(f"Task {key}: {value}")
