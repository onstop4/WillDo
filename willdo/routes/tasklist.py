from flask import Blueprint, render_template, redirect, url_for, request, g
from datetime import datetime
from collections import namedtuple
from ..db import IndividualTask
from .queries import query_tasks, get_tasklist_by_id, get_task_by_id, get_multiple_tasks_by_id
from .operations import bulk_change_completion_status, bulk_delete, remove_excess_whitespace
from .forms import validate_task


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
    task.description = remove_excess_whitespace(submitted_form.get('description'))
    task.priority = remove_excess_whitespace(submitted_form.get('priority'))
    task.completion_date = remove_excess_whitespace(get_date_from_str(submitted_form.get('completion-date')))
    task.creation_date = remove_excess_whitespace(get_date_from_str(submitted_form.get('creation-date')))

    return task


def delete_tasklist(tasklist_id):
    """Deletes tasklist with the associated tasklist_id. The results
    of this change are then committed to the database.

    :param tasklist_id: The id of the associated tasklist.
    """

    db_session = g.db_session

    tasklist = get_tasklist_by_id(tasklist_id)
    db_session.delete(tasklist)
    db_session.commit()


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


@bp.route('/<tasklist_id>/search/<term>/')
def search_tasks(tasklist_id, term):
    tasklist = get_tasklist_by_id(tasklist_id)
    tasklist_name = tasklist.name
    
    term = remove_excess_whitespace(term)
    query = query_tasks(tasklist, search_for=term)
    tasks = iter_tasks_for_html(query)

    return render_template('within_tasklist/select_task.html', tasklist_id=tasklist_id, tasklist_name=tasklist_name, tasks=tasks, search_term=term)


@bp.route('/<tasklist_id>/edit/newtask/', methods=['GET', 'POST'])
def create_task(tasklist_id):
    invalid = False
    if request.method == 'POST':
        submitted_form = request.form

        if validate_task(submitted_form):
            task = IndividualTask(description="")
            modify_task_from_form(submitted_form, task)
            task.tasklist_id = tasklist_id
            
            db_session = g.db_session
            db_session.add(task)
            db_session.commit()

            return redirect(url_for('tasklist_bp.list_tasks', tasklist_id=tasklist_id))
        else:
            invalid = True
    
    tasklist_name = get_tasklist_by_id(tasklist_id).name
    return render_template('within_tasklist/create_edit_task.html', tasklist_name=tasklist_name, invalid=invalid)


@bp.route('/<tasklist_id>/edit/edittask/<task_id>/', methods=['GET', 'POST'])
def edit_task_details(tasklist_id, task_id):
    db_session = g.db_session
    task = get_task_by_id(task_id)
    invalid = False

    if request.method == 'POST':
        submitted_form = request.form

        if validate_task(submitted_form):
            modify_task_from_form(submitted_form, task)
            db_session.commit()
            return redirect(url_for('tasklist_bp.list_tasks', tasklist_id=tasklist_id))
        else:
            invalid = True

    rtask = RenderedTask(task.id, task.is_complete, task.priority, task.completion_date, task.creation_date, task.description)
    tasklist_name = get_tasklist_by_id(tasklist_id).name
    return render_template('within_tasklist/create_edit_task.html', task=rtask, tasklist_name=tasklist_name, invalid=invalid)


@bp.route('/<tasklist_id>/edit', methods=['GET', 'POST'])
def perform_edit_action(tasklist_id):
    if request.method == 'POST':
        submitted_form = request.form

        if submitted_form.get('create-task'):
            return redirect(url_for('tasklist_bp.create_task', tasklist_id=tasklist_id))

        db_session = g.db_session

        task_ids = submitted_form.getlist('task-selected')
        tasks = get_multiple_tasks_by_id(task_ids)

        if submitted_form.get('search'):  # pylint: disable=no-else-return
            search_term = submitted_form.get('search-input', '')
            return redirect(url_for('tasklist_bp.search_tasks', tasklist_id=tasklist_id, term=search_term))
        elif submitted_form.get('mark-tasks-complete'):
            bulk_change_completion_status(tasks, True)
        elif submitted_form.get('mark-tasks-incomplete'):
            bulk_change_completion_status(tasks, False)
        elif submitted_form.get('delete-tasks'):
            bulk_delete(tasks)
        elif submitted_form.get('edit-tasklist'):
            return redirect(url_for('mainpage_bp.edit_tasklist_details', tasklist_id=tasklist_id))
        elif submitted_form.get('delete-tasklist'):
            delete_tasklist(tasklist_id)
            return redirect(url_for('mainpage_bp.select_tasklist'))

        db_session.commit()

    return redirect(url_for('tasklist_bp.list_tasks', tasklist_id=tasklist_id))


@bp.route('/<tasklist_id>/edit/togglecompletion/<task_id>/')
def toggle_task_completion(tasklist_id, task_id):
    task = get_task_by_id(task_id)
    task.is_complete = not task.is_complete

    return redirect(url_for('tasklist_bp.list_tasks', tasklist_id=tasklist_id))
