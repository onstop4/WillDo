from flask import Blueprint, render_template, redirect, url_for, request, g
from datetime import datetime
from collections import namedtuple
from ..db import IndividualTask
from .queries import query_tasks, get_tasklist_by_id, get_task_by_id, get_multiple_tasks_by_id
from .operations import bulk_change_completion_status, bulk_delete


bp = Blueprint('tasklist_bp', __name__)

RenderedTask = namedtuple('Individual_Task', ['id', 'is_complete', 'priority', 'completion_date', 'creation_date', 'description'])


def get_date_from_str(string):
    if string:
        date_format = r'%Y-%m-%d'  # format string is equivalent to the one used by date.fromisoformat() in Python 3.7+
        return datetime.strptime(string, date_format)


def format_date_as_str(string):
    if string:
        date_format = r'%Y-%m-%d'  # format string is equivalent to the one used by date.fromisoformat() in Python 3.7+
        return datetime.strftime(string, date_format)


def modify_task_from_form(submitted_form, task: IndividualTask):
    task.description = submitted_form.get('description')
    task.priority = submitted_form.get('priority')
    task.completion_date = get_date_from_str(submitted_form.get('completion-date'))
    task.creation_date = get_date_from_str(submitted_form.get('creation-date'))

    return task


def iter_tasks_for_html(query):
    for instance in query:
        _id = instance.id
        is_complete = instance.is_complete
        priority = instance.priority
        completion_date = instance.completion_date
        creation_date = instance.creation_date
        description = instance.description
        yield RenderedTask(_id, is_complete, priority, completion_date, creation_date, description)


@bp.route('/<tasklist_id>/')
def list_tasks(tasklist_id):
    tasklist = get_tasklist_by_id(tasklist_id)
    tasklist_name = tasklist.name
    
    query = query_tasks(tasklist)
    tasks = iter_tasks_for_html(query)

    return render_template('within_tasklist/select_task.html', tasklist_id=tasklist_id, tasklist_name=tasklist_name, tasks=tasks)


@bp.route('/<tasklist_id>/edit/newtask/', methods=['GET', 'POST'])
def create_task(tasklist_id):
    if request.method == 'POST':
        submitted_form = request.form
        
        task = IndividualTask(description="")
        modify_task_from_form(submitted_form, task)
        task.tasklist_id = tasklist_id
        
        db_session = g.db_session
        db_session.add(task)
        db_session.commit()

        return redirect(url_for('tasklist_bp.list_tasks', tasklist_id=tasklist_id))
    
    return render_template('within_tasklist/create_edit_task.html')


@bp.route('/<tasklist_id>/edit/edittask/<task_id>/', methods=['GET', 'POST'])
def edit_task_details(tasklist_id, task_id):
    db_session = g.db_session
    task = get_task_by_id(task_id)

    if request.method == 'POST':
        submitted_form = request.form
        
        modify_task_from_form(submitted_form, task)
        
        db_session.commit()

        return redirect(url_for('tasklist_bp.list_tasks', tasklist_id=tasklist_id))
    
    rtask = RenderedTask(task.id, task.is_complete, task.priority, task.completion_date, task.creation_date, task.description)
    return render_template('within_tasklist/create_edit_task.html', task=rtask)


@bp.route('/<tasklist_id>/edit', methods=['GET', 'POST'])
def perform_edit_action(tasklist_id):
    if request.method == 'POST':
        submitted_form = request.form

        if submitted_form.get('create-task'):
            return redirect(url_for('tasklist_bp.create_task', tasklist_id=tasklist_id))

        db_session = g.db_session

        task_ids = submitted_form.getlist('task-selected')
        tasks = get_multiple_tasks_by_id(task_ids)

        if submitted_form.get('mark-tasks-complete'):
            bulk_change_completion_status(tasks, True)
        elif submitted_form.get('mark-tasks-incomplete'):
            bulk_change_completion_status(tasks, False)
        elif submitted_form.get('delete-tasks'):
            bulk_delete(tasks)
        
        db_session.commit()

    return redirect(url_for('tasklist_bp.list_tasks', tasklist_id=tasklist_id))


@bp.route('/<tasklist_id>/edit/deletetask/<task_id>')
def delete_task(tasklist_id, task_id):
    return redirect(url_for('tasklist_bp.list_tasks', tasklist_id=tasklist_id))


@bp.route('/<tasklist_id>/edit/togglecompletion/<task_id>/')
def toggle_task_completion(tasklist_id, task_id):
    task = get_task_by_id(task_id)
    task.is_complete = not task.is_complete

    return redirect(url_for('tasklist_bp.list_tasks', tasklist_id=tasklist_id))
