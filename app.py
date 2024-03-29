from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
# from error import InvalidParameter
from flask_api import status
import json
from flask_cors import CORS, cross_origin
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.sqlite')

cors = CORS(app)
app.config['SECRET_KEY'] = 'thisissecret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo/todo.db'
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean, default=False)


@app.route('/', methods=['GET'])
def get_all_tasks():
    filters = {
        "ALL": "all",
        "COMPLETED": "completed",
        "NOT_COMPLETED": "not_completed"
    }

    page_size = request.args.get('page_size', None)
    current_page = request.args.get('current_page', None)
    filter = request.args.get('filter', None).lower().replace(" ", "")

    if filter == filters["ALL"]:
        task_query = Task.query.paginate(int(current_page), int(page_size), False)

    elif filter == filters["COMPLETED"]:
        task_query = Task.query.filter_by(complete=True).paginate(int(current_page), int(page_size), False)

    elif filter == filters["NOT_COMPLETED"]:
        task_query = Task.query.filter_by(complete=False).paginate(int(current_page), int(page_size), False)

    else:
        return make_response(jsonify("Filter not found"), 404)

    task_items = task_query.items
    total = len(task_items)

    output = []

    for task in task_items:
        task_data = {}
        task_data['id'] = task.id
        task_data['name'] = task.name
        task_data['content'] = task.content
        task_data['complete'] = task.complete
        output.append(task_data)

    response = jsonify({
        "total": total,
        "page_size": int(page_size),
        "current_page": int(current_page),
        "items": output
    })

    return response, status.HTTP_201_CREATED


@app.route('/task/<id>', methods=['GET'])
def get_one_task(id):
    task = Task.query.filter_by(id=id).first()

    if not task:
        return make_response(jsonify("id not found"), 404)

    return make_response(jsonify(taks), 200)


@app.route('/task', methods=['POST'])
def create_user():
    data = request.get_json()

    new_task = Task(name=data['name'], content=data['content'], complete=False)
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify("New task created"), 200)


@app.route('/task/<id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()

    name = data.get('name', None)
    content = data.get('content', None)
    complete = data.get('complete', None)
    task = Task.query.filter_by(id=id).first()

    if not task:
        make_response(jsonify("Task not found"), 404)

    task.name = name
    task.content = content
    task.complete = complete

    db.session.commit()

    return make_response(jsonify("Updated."), 200)


@app.route('/task/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.filter_by(id=id).first()

    if not task:
        make_response(jsonify("Task id not found."), 404)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify("Deleted."), 200)


if __name__ == '__main__':
    app.run(debug=True)
