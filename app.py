import mysql.connector
from datetime import datetime, timedelta
import json

# Connect Ke Database
db = mysql.connector.connect(host="localhost", user="root", password="", database="kka")

cursor = db.cursor()


# menghitung Cost dengan A*
def calculate_cost(task):
    current_date = datetime.now().date()
    heuristic = 0

    if task[3] == "Importance":
        heuristic += 1
    elif task[3] == "Not importance":
        heuristic += 3

    if task[4] == "Urgent":
        heuristic += 1
    elif task[4] == "Not urgent":
        heuristic += 3

    deadline_diff = (task[2] - current_date).days
    heuristic += deadline_diff

    cost = heuristic
    return cost


# Select Data dari DB
cursor.execute("SELECT * FROM tasks")
tasks = cursor.fetchall()

# Menghitung Cost dari table tasks
tasks_with_cost = []
for task in tasks:
    cost = calculate_cost(task)
    tasks_with_cost.append({"task": task, "cost": cost})

# Sorting table tasks
tasks_with_cost.sort(key=lambda x: x["cost"])

# Update Table Tasks
for index, task in enumerate(tasks_with_cost):
    cursor.execute(
        "UPDATE tasks SET taskPriority = %s WHERE taskName = %s",
        (index + 1, task["task"][0]),
    )

# Filter tugas yang deadline nya tidak lewat
filtered_tasks = []
for item in tasks_with_cost:
    deadline_diff = (item["task"][2] - datetime.now().date()).days
    if deadline_diff >= 0:
        filtered_tasks.append(
            {
                "priority": item["task"][5],
                "task_name": item["task"][0],
                "subject": item["task"][1],
                "days_left": deadline_diff,
            }
        )

# Print data dari JSON
with open("tasks.json", "w") as json_file:
    json.dump(filtered_tasks, json_file, indent=2)

# Exception menghapus tugas yang deadline nya lewat
cursor.execute("DELETE FROM tasks WHERE deadline <= CURDATE()")

# Commit ke DB
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()
