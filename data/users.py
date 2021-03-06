import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    data = sqlalchemy.Column(sqlalchemy.String, default="costs = {}")

    def __repr__(self):
        return ' '.join(
            [self.username, self.email, self.hashed_password])

    def check_password(self, trying_pass):
        if trying_pass == self.hashed_password:
            return True
        else:
            return False
