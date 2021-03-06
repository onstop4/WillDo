from flask import Blueprint, render_template, g, url_for, request, redirect
from collections import namedtuple
from ..db import AvailableTasklist
from .queries import query_tasklists, get_tasklist_by_id
from .operations import remove_excess_whitespace
from .forms import validate_tasklist


bp = Blueprint('mainpage_bp', __name__)

RenderedTasklist = namedtuple('Available_Tasklist', ['id', 'name'])


def iter_tasklists_for_html(query):
    for instance in query:
        _id = instance.id
        name = instance.name
        yield RenderedTasklist(_id, name)


def modify_tasklist_from_form(submitted_form, tasklist: AvailableTasklist):
    tasklist.name = remove_excess_whitespace(submitted_form.get('name'))
    return tasklist


@bp.route('/')
def select_tasklist():
    query = query_tasklists()
    tasklists = iter_tasklists_for_html(query)
    return render_template('select_tasklist.html', tasklists=tasklists)


@bp.route('/search', methods=['GET', 'POST'])
def process_search():
    if request.method == 'POST': # pylint: disable=no-else-return
        submitted_form = request.form
        term = submitted_form.get('search-input', '')
        return redirect(url_for('mainpage_bp.search_for_tasklist', term=term))

    else:
        return redirect(url_for('mainpage_bp.select_tasklist'))


@bp.route('/search/<term>/')
def search_for_tasklist(term):
    term = remove_excess_whitespace(term)
    query = query_tasklists(search_for=term)
    tasklists = iter_tasklists_for_html(query)
    return render_template('select_tasklist.html', tasklists=tasklists, search_term=term)


@bp.route('/edit/newlist/', methods=['GET', 'POST'])
def create_tasklist():
    invalid = False
    if request.method == 'POST':
        submitted_form = request.form

        if validate_tasklist(submitted_form):
            tasklist = AvailableTasklist(name='')
            modify_tasklist_from_form(submitted_form, tasklist)

            db_session = g.db_session
            db_session.add(tasklist)
            db_session.commit()

            return redirect(url_for('mainpage_bp.select_tasklist'))
        else:
            invalid = True

    return render_template('create_edit_tasklist.html', invalid=invalid)


@bp.route('/edit/<tasklist_id>/', methods=['GET', 'POST'])
def edit_tasklist_details(tasklist_id):
    tasklist = get_tasklist_by_id(tasklist_id)
    tasklist_name = tasklist.name
    invalid = False

    if request.method == 'POST':
        db_session = g.db_session
        submitted_form = request.form
        if validate_tasklist(submitted_form):
            modify_tasklist_from_form(submitted_form, tasklist)

            db_session.commit()
            return redirect(url_for('tasklist_bp.list_tasks', tasklist_id=tasklist_id))
        else:
            invalid = True

    return render_template('create_edit_tasklist.html', tasklist_name=tasklist_name, invalid=invalid)
