from flask import Flask
from apps.setting import sqlurl
from apps.index.index import index
from apps.admin.admin import admin
from apps.api.api import api
# from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sqlurl
app.config['SQLALCHEMY_POOL_RECYCLE'] = 499
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.register_blueprint(index,url_prefix = '/')
app.register_blueprint(admin,url_prefix = '/admin')
app.register_blueprint(api,url_prefix = '/api')




if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000 ,debug = True)
