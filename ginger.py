# encoding: utf-8
from http.client import HTTPException

from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError

app = create_app()


# 捕捉异常
@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
