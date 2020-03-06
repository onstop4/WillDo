# pylint: skip-file

from flask import current_app
from willdo import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', threaded=False)
