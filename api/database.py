from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class DB(SQLAlchemy):
    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def update(self, obj):
        self.session.commit()


db = DB()


def get_db(app: Flask):
    db.init_app(app)
    return app, db
