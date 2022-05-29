from datetime import timedelta, datetime, timezone

from flask import Flask
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, get_jwt_identity, set_access_cookies

from .config import config
from .database import get_db

from .admin.admin import admin
from .authentication.authentication import auth
from .content.content import content
from .create.create import create

from .models.users import *

app = Flask(__name__)
app.config.update(config)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_IDENTITY_CLAIM"] = "user_id"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

app, db = get_db(app)
app.app_context().push()

jwt = JWTManager(app)

for blueprint in [auth, admin, content, create]:
    app.register_blueprint(blueprint)


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data[app.config["JWT_IDENTITY_CLAIM"]]
    return User.query.get(identity)


@app.after_request
def refresh_tokens(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(hours=12))

        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
            return response
    except (RuntimeError, KeyError):
        return response


@app.route("/")
def index():
    return "Hello, World", 200


#db.drop_all()
db.create_all()
