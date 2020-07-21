from flask import Blueprint, render_template, g, url_for, request, redirect
from collections import namedtuple
from ..db import AvailableTasklist
from .queries import query_tasklists
from .operations import remove_excess_whitespace
from .forms import validate_tasklist


bp = Blueprint('mainpage_bp', __name__)

RenderedTasklist = namedtuple('Available_Tasklist', ['id', 'name'])


def iter_tasklists_for_html(query):
    for instance in query:
        _id = instance.id
        name = instance.name
        yield RenderedTasklist(_id, name)


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
    if request.method == 'POST':
        submitted_form = request.form
        if not validate_tasklist(submitted_form):
            return render_template('create_edit_tasklist.html', invalid=True)

        name = remove_excess_whitespace(submitted_form['name'])

        tasklist = AvailableTasklist(name=name)

        db_session = g.db_session
        db_session.add(tasklist)
        db_session.commit()

        return redirect(url_for('mainpage_bp.select_tasklist'))

    return render_template('create_edit_tasklist.html')
