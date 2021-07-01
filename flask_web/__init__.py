from flask import Flask, session
from flask_wtf.csrf import CSRFProtect
from flaskext.mysql import MySQL
from flask_web.server import WebServer

app = Flask(__name__, static_folder="static")
app.config.update({
    "SECRET_KEY" : "81a2cd4169d3bbc6600b704c"
    })

app.config['MYSQL_DATABASE_HOST'] = ''
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'user_portfolio'
app.config['MYSQL_DATABASE_PORT'] = 3306

#CSSRF protect
csrf = CSRFProtect()
csrf.init_app(app)

#mySQL
mysql = MySQL()
mysql.init_app(app)

#init session
session = session

#init web server to process request
webserver = WebServer(mysql)

from flask_web import routes, auth

