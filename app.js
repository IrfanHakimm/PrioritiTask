import express, { json } from "express";
import { createConnection } from "mysql";
import { exec } from "child_process";

const app = express();
const port = 3000;

// MySQL Configuration
const mysqlConfig = {
  host: "your_mysql_host",
  user: "your_mysql_user",
  password: "your_mysql_password",
  database: "your_mysql_database",
};

// Create MySQL connection
const connection = createConnection(mysqlConfig);

// Connect to MySQL
connection.connect((err) => {
  if (err) {
    console.error("Error connecting to MySQL:", err);
    return;
  }
  console.log("Connected to MySQL");
});
// Handle adding a task
app.post("/addTask", json(), (req, res) => {
  const { taskName, subject, deadline, importance, urgency } = req.body;

  // Insert data into MySQL
  const sql =
    "INSERT INTO tasks (task_name, subject, deadline, importance, urgency) VALUES (?, ?, ?, ?, ?)";
  const values = [taskName, subject, deadline, importance, urgency];

  connection.query(sql, values, (err, result) => {
    if (err) {
      console.error("Error adding task to MySQL:", err);
      res.status(500).json({ error: "Internal Server Error" });
      return;
    }
    console.log("Task added to MySQL:", result);
    res.json({ success: true });
  });
});

// Handle generating a graph
app.post("/generateGraph", (req, res) => {
  // Trigger the Python script using child_process
  exec("python generate_graph.py", (error, stdout, stderr) => {
    if (error) {
      console.error("Error executing Python script:", error);
      res.status(500).json({ error: "Internal Server Error" });
      return;
    }
    const graphData = JSON.parse(stdout);
    console.log("Graph generated successfully:", graphData);
    res.json({ success: true, graphData });
  });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
