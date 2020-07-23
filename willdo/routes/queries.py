from enum import IntEnum
from flask import g
from sqlalchemy import func
from ..db import AvailableTasklist, IndividualTask


class Sort_Config(IntEnum):
    completion_date = 0
    id = 1
    priority = 2
    creation_date = 3
    description = 4


def query_tasklists(search_for=None):
    """Returns a query object for the rows of tasklists in
    the database. If :arg:`search_for` is truthy, the query
    is filtered for results that contain :arg:`search_for`
    (case-insensitive).

    :param str search_for: A string that the query is
                           filtered by.
    :return: Query object for tasklists.
    :rtype: sqlalchemy.orm.query.Query
    """

    db_session = g.db_session
    query = db_session.query(AvailableTasklist).order_by(
        AvailableTasklist.name)

    if search_for:
        search_for = search_for.lower()
        operation = func.lower(AvailableTasklist.name).contains(
            search_for, autoescape=True)
        query = query.filter(operation)

    return query


def query_tasks(tasklist, search_for=None):
    """Returns a query object for the rows of tasks in
    the database. If :arg:`search_for` is truthy, the query
    is filtered for results that contain :arg:`search_for`
    (case-insensitive).

    :param str search_for: A string that the query is
                           filtered by.
    :return: Query object for tasklists.
    :rtype: sqlalchemy.orm.query.Query
    """

    db_session = g.db_session
    query = db_session.query(IndividualTask).join(
        AvailableTasklist).filter(IndividualTask.tasklist_id == tasklist.id)
    query = query.order_by(IndividualTask.completion_date)

    if search_for:
        search_for = search_for.lower()
        operation = func.lower(IndividualTask.description).contains(
            search_for, autoescape=True)
        query = query.filter(operation)

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
