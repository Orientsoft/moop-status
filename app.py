# -*- coding:utf-8 -*-
from flask import Flask
from ext import falseReturn

app = Flask(__name__)
app.config.from_pyfile('config.py')

from applications.history import history

app.register_blueprint(history)


@app.errorhandler(Exception)
def error_handler(error):
    return falseReturn('服务异常')


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'], threaded=True)
