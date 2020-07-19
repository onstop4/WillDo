def bulk_change_completion_status(tasks, status: bool):
    for task in tasks:
        task.is_complete = status


def bulk_delete(tasks):
    pass


def remove_excess_whitespace(maybe_text):
    """Removes excess whitespace from maybe_text if this argument
    is a string.

    :param maybe_text: An object that might be a string.
    """

    if isinstance(maybe_text, str):
        maybe_text = ' '.join(maybe_text.split())
        maybe_text = maybe_text.strip()
    return maybe_text
