from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wenxingliu@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, server_default='false')

    def __repr__(self):
        return f'<Todo {self.id}: {self.description}>'


@app.route('/')
def index():
    todo_list = Todo.query.order_by('id').all()
    return render_template('index.html', data=todo_list)


@app.route('/todo/create', methods=['POST'])
def create_todo():
    error = False
    body = {}

    try:
        new_todo = Todo(description=request.get_json()['description'])
        db.session.add(new_todo)
        db.session.commit()
        body['description'] = new_todo.description
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    
    if error:
        abort (400)
    else:
        return jsonify(body)


@app.route('/todo/<todo_id>/set-completed', methods=['POST'])
def set_completed_status(todo_id):
    try:
        new_completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = new_completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


# @app.route('/todo/delete', methods=['POST'])
# def remove_item():
#     try:
#         todo_id = request.get_json()['id']
#         Todo.query.get(todo_id).delete()
#         db.session.commit()
#     except:
#         db.session.rollback()
#     finally:
#         db.session.close()
#     return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=8001, debug=True)

