from flask import g
from ..db import AvailableTasklist, IndividualTask


def query_tasklists(search_for=None):
    db_session = g.db_session
    query = db_session.query(AvailableTasklist).order_by(AvailableTasklist.name)
    
    if search_for:
        query = query.filter(AvailableTasklist.name.ilike('%{}%'.format(search_for)))
    
    return query


def query_tasks(tasklist, search_for=None):
    db_session = g.db_session
    query = db_session.query(IndividualTask).join(AvailableTasklist).filter(IndividualTask.tasklist_id == tasklist.id)
    query = query.order_by(IndividualTask.completion_date)

    if search_for:
        query = query.filter(IndividualTask.name.ilike('%{}%'.format(search_for)))

    return query


def get_tasklist_by_id(tasklist_id):
    db_session = g.db_session
    return db_session.query(AvailableTasklist).filter_by(id=tasklist_id).first()


def get_task_by_id(task_id):
    db_session = g.db_session
    return db_session.query(IndividualTask).filter_by(id=task_id).first()

def get_multiple_tasks_by_id(task_ids):
    for task_id in task_ids:
        task = get_task_by_id(task_id)
        yield task
