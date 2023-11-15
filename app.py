import mysql.connector
from datetime import datetime

def generateTable():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kka"
    )

    taskNames = []
    subjects = []
    dl = []
    importancies = []
    urgencies = []

    temp = db.cursor()
    temp.execute("SELECT * FROM tasks")

    for row in temp:
        taskNames.append(row[0])
        subjects.append(row[1])
        importancies.append(row[3])
        urgencies.append(row[4])

        deadline = row[2]
        curr_date = datetime.now().date()
        days_until_deadline = (deadline - curr_date).days
        dl.append(days_until_deadline)

    temp.close()

    return taskNames, subjects, dl, importancies, urgencies

taskNames, subjects, dl, importancies, urgencies = generateTable()

print("Task Names:", taskNames)
print("Subjects:", subjects)
print("Deadlines:", dl)
print("Importances:", importancies)
print("Urgencies:", urgencies)
