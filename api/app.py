from flask import Flask
from flask_jwt_extended import JWTManager

from .config import config
from .database import get_db

from .admin.admin import admin
from .authentication.authentication import auth
from .content.content import content
from .create.create import create

from .models.users import *

app = Flask(__name__)
app.config.update(config)

app, db = get_db(app)
app.app_context().push()

jwt = JWTManager(app)

for blueprint in [auth, admin, content, create]:
    app.register_blueprint(blueprint)


@app.route("/")
def index():
    return "Hello, World", 200


db.create_all()
