import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    questions = orm.relation("Question", back_populates='user')

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.String, default='Operator')

    def __repr__(self):
        return ' '.join(
            [self.username, self.email, self.hashed_password])

    def check_password(self, trying_pass):
        if trying_pass == self.hashed_password:
            return True
        else:
            return False
