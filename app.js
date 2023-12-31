const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql");
const { spawn } = require("child_process");
const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.set("view engine", "ejs");
app.set("views", "views");

// Connect ke MySQL
const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "",
  database: "kka",
});

// Check if connected
db.connect((err) => {
  if (err) {
    console.error("Error connecting to MySQL:", err);
    return;
  }
  console.log("Connected to MySQL");

  // Local data connection
  app.get("/", (req, res) => {
    try {
      const tasks = require("./tasks.json");
      res.render("index", { tasks });
    } catch (error) {
      console.error("Error loading local data:", error);
      res.status(500).send("Internal Server Error");
    }
  });

  // post request buat add task dari user
  app.post("/addTask", (req, res) => {
    const insertTask = `INSERT INTO tasks (taskName, subject, deadline, importance, urgency) VALUES ('${req.body.taskName}', '${req.body.subject}', '${req.body.deadline}', '${req.body.importance}', '${req.body.urgency}');`;

    db.query(insertTask, (err, result) => {
      if (err) {
        console.error("Error executing query:", err);
        res.status(500).send("Internal Server Error");
        return;
      }

      console.log("Task Inserted successfully");
      res.redirect("/");
    });
  });

  // get request buat generate table
  app.get("/generateTable", (req, res) => {
    // Call Python script when the button is pressed
    const pythonProcess = spawn("python", ["app.py"]);

    pythonProcess.stdout.on("data", (data) => {
      console.log(`Python script output: ${data}`);
    });

    pythonProcess.stderr.on("data", (data) => {
      console.error(`Error in Python script: ${data}`);
    });

    pythonProcess.on("close", (code) => {
      console.log(`Python script process exited with code ${code}`);
      // Redirect or send a response to the client as needed
      res.redirect("/");
    });
  });
});

// jika running akan memunculkan localhost server
app.listen(8000, () => {
  console.log(`Server is running on http://localhost:${8000}`);
});
