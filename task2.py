from task1 import tasks
from flask import Flask, jsonify, abort, request
import datetime
app = Flask(__name__)

#Update Task Status To Done
def mark(task, status, task_id):
    if task_id == task["id"]:
        task["done"] = status

    return task


@app.route("/todo/mark/<int:task_id>/<int:status>", methods=["PUT"])
def mark_task(task_id, status):

    global tasks
    if status == 1:
        status = True
    else:
        status = False

    tasks = [mark(task, status, task_id) for task in tasks]

    return jsonify(tasks)
    
#Add Due Date To Tasks

@app.route('/todo', methods=["POST"])
def add_todo():
    if not request.json:
        abort(500)

    title = request.json.get("title", None)
    desc = request.json.get("description", "")
    due = request.json.get("due" ,None)
    if due is not None:
        due = datetime.datetime.strptime(due, "%d-%m-%Y")
    else:
        due = datetime.datetime.now()


    global tasks
    tasks.append({
        "id": len(tasks) + 1,
        "title": title,
        "description": desc,
        "done": False,
        "due" : due
    })
    return jsonify(len(tasks)) 

#SORT TASKS AS PER DUE DATE

def sort_due_date(x):
    return x["due"]


@app.route('/todo', methods=["GET"])
@app.route('/todo/<string:direction>', methods=["GET"])
def todo(direction=None):
    # direction is optional

    if direction == "ASC":
        direction = True
    else:
        direction = False

    global tasks
    if direction is not None:
        tasks.sort(reverse=direction, key=sort_due_date)

    return jsonify(tasks) 
    
if __name__ == '__main__':
    app.run(debug=True)