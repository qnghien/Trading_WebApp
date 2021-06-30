from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flaskext.mysql import MySQL

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

from flask_web import routes
from flask_web import auth