from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, static_folder="static")
app.config.update({
    "SECRET_KEY" : "81a2cd4169d3bbc6600b704c"
    })

#CSSRF protect
csrf = CSRFProtect()
csrf.init_app(app)

from flask_web import routes