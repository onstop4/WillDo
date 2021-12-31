# WillDo
An experimental browser-based todo app without any JavaScript. Built using [Flask](https://flask.palletsprojects.com).

## Requirements
The Python requirements can be installed by running:
```
pip install -r requirements.txt
```
To run WillDo on the Flask development server, run the following commands:
```
export FLASK_APP=willdo
flask run
```
The value for `SQLALCHEMY_DATABASE_URI` needs to be set in the `instance/config.py` file for WillDo to work.
