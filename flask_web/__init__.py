from flask import Flask, session
from flask_wtf.csrf import CSRFProtect
from flask_web.server import WebServer


app = Flask(__name__, static_folder="static")
app.config.update({
    "SECRET_KEY" : "81a2cd4169d3bbc6600b704c"
    })

# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'ducanh2001'
# app.config['MYSQL_DATABASE_DB'] = 'user_portfolio'
# app.config['MYSQL_DATABASE_PORT'] = 3306


#CSSRF protect---------------------------------------------------------------
csrf = CSRFProtect()
csrf.init_app(app)

#Database ----------------------------------------------------------------------
#from flaskext.mysql import MySQL
# mydatabse = MySQL()
# mydatabse.init_app(app)

import psycopg2 
mydatabse = psycopg2.connect(
    host='plot.ch1wzlgi5g91.ap-southeast-1.rds.amazonaws.com',
    database="plot",
    user="plot",
    password="plot123456",
    port=5432)

#init session-----------------------------------------------------------------
session = session

#init web server to process request
webserver = WebServer(mydatabse)

from flask_web import routes, auth