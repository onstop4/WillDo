from wtforms import Form, StringField
from wtforms.validators import InputRequired, Regexp


BASIC_INPUT_REGEX = r'^.*\w.*$'
PRIORITY_INPUT_REGEX = r'^[A-Z]$'
DATE_INPUT_REGEX = r'^\d{4}-\d{2}-\d{2}$'


class TasklistForm(Form):
    name = StringField(validators=[InputRequired(), Regexp(BASIC_INPUT_REGEX)])


class TaskForm(Form):
    priority = StringField(validators=[Regexp(PRIORITY_INPUT_REGEX)])
    completion_date = StringField(validators=[Regexp(DATE_INPUT_REGEX)])
    creation_date = StringField(validators=[Regexp(DATE_INPUT_REGEX)])
    description = StringField(
        validators=[InputRequired(), Regexp(BASIC_INPUT_REGEX)])
