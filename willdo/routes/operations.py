def bulk_change_completion_status(tasks, status: bool):
    for task in tasks:
        task.is_complete = status


def bulk_delete(tasks):
    pass
