from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, Boolean

from api.database import DB, db

db: DB


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text)
    email = Column(Text)
    password = Column(Text)
    is_admin = Column(Boolean)

    @staticmethod
    def create(username: str, email: str, password: str, is_admin: str):
        user = User(
            username=username,
            email=email,
            password=password,
            is_admin=is_admin
        )

        db.add(user)

    def __repr__(self):
        return f"<User {self.username}>"
