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


def remove_excess_whitespace(maybe_text):
    """Removes excess whitespace from maybe_text if this argument
    is a string.

    :param maybe_text: An object that might be a string.
    """

    if isinstance(maybe_text, str):
        maybe_text = ' '.join(maybe_text.split())
        maybe_text = maybe_text.strip()
    return maybe_text
