from flask import render_template, request, redirect, url_for, jsonify, abort

from config import db, app, migrate


class Todo(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, server_default='false')
    list_id = db.Column(db.Integer, db.ForeignKey('todolist.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id}: {self.description}>'


class TodoList(db.Model):
	__tablename__ = 'todolist'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(), nullable=False)
	todo = db.relationship('todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<Todo List {self.id}: {self.name}>'
