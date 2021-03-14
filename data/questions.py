import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    author_username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    personal = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    answered = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user = orm.relation('User')


    def __repr__(self):
        return ' '.join(
            [str(self.user_id), self.text])
