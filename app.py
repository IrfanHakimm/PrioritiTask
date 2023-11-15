import mysql.connector
from datetime import datetime
from tabulate import tabulate

# Connect to the database
db = mysql.connector.connect(host="localhost", user="root", password="", database="kka")

# Add 'taskPriority' column to the 'tasks' table if it doesn't exist
cursor = db.cursor()


# Function to calculate cost based on A* algorithm
def calculate_cost(task):
    current_date = datetime.now().date()
    heuristic = 0
    if task[3] == "Importance":
        heuristic += 2
    if task[4] == "Urgent":
        heuristic += 1
    else:
        heuristic += 3
    cost = (task[2] - current_date).days + heuristic
    return cost

# Retrieve data from the database
cursor.execute("SELECT * FROM tasks")
tasks = cursor.fetchall()

# Add 'taskPriority' to each task
for index, task in enumerate(tasks):
    cursor.execute(
        "UPDATE tasks SET taskPriority = %s WHERE taskName = %s", (index + 1, task[0])
    )

# Calculate and store costs for each task
tasks_with_cost = []
for task in tasks:
    cost = calculate_cost(task)
    tasks_with_cost.append((task, cost))

# Sort tasks based on cost
tasks_with_cost.sort(key=lambda x: x[1])

# Display prioritized tasks using tabulate
table_data = []
for index, (task, cost) in enumerate(tasks_with_cost):
    deadline_diff = (task[2] - datetime.now().date()).days
    if deadline_diff >= 0:
        table_data.append([index + 1, task[0], task[1], deadline_diff])

# Define headers for the tabulated data
headers = ["Priority", "Task Name", "Subject", "Days Left"]

# Print the tabulated data
print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

# Drop columns for tasks with passed deadlines
cursor.execute("DELETE FROM tasks WHERE deadline < CURDATE()")

# Commit the changes to the database
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()
