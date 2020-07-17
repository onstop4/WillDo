from wtforms import Form, StringField
from wtforms.validators import InputRequired, Optional, Regexp
from werkzeug.datastructures import MultiDict


BASIC_INPUT_REGEX = r'^.*\w.*$'
PRIORITY_INPUT_REGEX = r'^[A-Z]$'
DATE_INPUT_REGEX = r'^\d{4}-\d{2}-\d{2}$'

key_association = {
    'completion-date': 'completion_date',
    'creation-date': 'creation_date'
}


def convert_associated_keys(form_input: MultiDict):
    """Returns a :class:`MultiDict` with keys converted according to
    :obj:`key_association`. The original keys are still present,
    along with any keys not found in :obj:`key_association`. This
    function is meant to resolve the scenario where the keys present
    in the form response don't match the attributes in the WTForms
    :class:`Form` classes.

    :param MultiDict form_input: The submitted form inputs.
    :return: A MultiDict with the old and the new ("converted") keys.
    :rtype: MultiDict
    """

    new_form_input = form_input.copy()
    for key in form_input.keys():
        new_key = key_association.get(key, key)
        new_form_input[new_key] = form_input[key]
    return new_form_input


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

    form_input = MultiDict(form_input)
    form_input = convert_associated_keys(form_input)
    form = TasklistForm(form_input)
    return form.validate()


def validate_task(form_input: MultiDict):
    """Checks if form inputs are valid for a task.

    :param MultiDict form_input: The submitted form inputs.
    :return: Whether form inputs are valid.
    :rtype: bool
    """

    form_input = MultiDict(form_input)
    form_input = convert_associated_keys(form_input)
    form = TaskForm(form_input)
    return form.validate()
