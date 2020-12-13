from flask import render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

from config import db, app, migrate
from models.todos import Todo

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
        body['id'] = new_todo.id
        body['description'] = new_todo.description
        body['completed'] = new_todo.completed
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


@app.route('/todo/<todo_id>', methods=['DELETE'])
def remove_item(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })



if __name__ == '__main__':
    app.run(port=8001, debug=True)

