from wtforms import Form, StringField
from wtforms.validators import InputRequired, Optional, Regexp
from werkzeug.datastructures import MultiDict


BASIC_INPUT_REGEX = r'^.*\w.*$'
PRIORITY_INPUT_REGEX = r'^[A-Z]$'
DATE_INPUT_REGEX = r'^\d{4}-\d{2}-\d{2}$'


class TasklistForm(Form):
    name = StringField(validators=[InputRequired(), Regexp(BASIC_INPUT_REGEX)])


class TaskForm(Form):
    priority = StringField(
        validators=[Optional(), Regexp(PRIORITY_INPUT_REGEX)])
    completion_date = StringField(
        validators=[Optional(), Regexp(DATE_INPUT_REGEX)])
    creation_date = StringField(
        validators=[Optional(), Regexp(DATE_INPUT_REGEX)])
    description = StringField(
        validators=[InputRequired(), Regexp(BASIC_INPUT_REGEX)])


def validate_tasklist(form_input: MultiDict):
    """Checks if form inputs are valid for a tasklist.

    :param MultiDict form_input: The submitted form inputs.
    :return: Whether form inputs are valid.
    :rtype: bool
    """

    form = TasklistForm(form_input)
    return form.validate()


def validate_task(form_input: MultiDict):
    """Checks if form inputs are valid for a task.

    :param MultiDict form_input: The submitted form inputs.
    :return: Whether form inputs are valid.
    :rtype: bool
    """

    form = TaskForm(form_input)
    return form.validate()
