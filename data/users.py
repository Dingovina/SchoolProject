import sqlalchemy
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    username = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return ' '.join(
            [self.username, self.email, self.hashed_password])
