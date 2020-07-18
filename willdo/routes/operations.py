from flask import g


def bulk_change_completion_status(tasks, status: bool):
    for task in tasks:
        task.is_complete = status


def bulk_delete(tasks):
    """Bulk delete multiple tasks. The tasks don't have to
    be in the same tasklist (although the user should
    only be allowed to delete from same tasklist). Changes
    still have to be committed to database.

    :param tasks:
        An iterable yielding Task objects (representing
        rows in database.)
    """

    db_session = g.db_session

    for task in tasks:
        db_session.delete(task)
