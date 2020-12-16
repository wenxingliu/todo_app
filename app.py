from flask import render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

from config import db, app, migrate
from models.todos import Todo, TodoList

@app.route('/')
def index():
    return redirect(url_for('get_list', list_id=1))


@app.route('/list/<list_id>')
def get_list(list_id):
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()
    lists = TodoList.query.order_by('id').all()
    active_list = TodoList.query.get(list_id)
    return render_template('index.html', active_list=active_list, todos=todos, lists=lists)


@app.route('/list/create', methods=['POST'])
def create_list():
    error = False
    body = {}

    try:
        new_list = TodoList(name=request.get_json()['name'])
        db.session.add(new_list)
        db.session.commit()
        body['id'] = new_list.id
        body['name'] = new_list.name
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort (400)
    else:
        return jsonify(body)


@app.route('/list/<list_id>/set-completed', methods=['POST'])
def set_completed_status_list(list_id):
    try:
        new_completed_status = request.get_json()['completed']
        selectedList = TodoList.query.get(list_id)
        selectedList.completed = new_completed_status

        list_todos = Todo.query.filter_by(list_id=list_id)
        for todo in list_todos:
            todo.completed = new_completed_status
        
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('get_list', list_id=list_id))


@app.route('/list/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    error = False
    try:
        Todo.query.filter_by(list_id=list_id).delete()
        TodoList.query.filter_by(id=list_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort (400)
    else:
        return jsonify({ 'success': True })


@app.route('/todo/create', methods=['POST'])
def create_todo():
    error = False
    body = {}

    try:
        new_todo = Todo(description=request.get_json()['description'],
                        list_id=request.get_json()['list_id'])
        db.session.add(new_todo)
        db.session.commit()
        body['id'] = new_todo.id
        body['list_id'] = new_todo.list_id
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
def set_completed_status_todo(todo_id):
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

