import sqlalchemy
from .db_session import SqlAlchemyBase


class Cell(SqlAlchemyBase):
    __tablename__ = 'cells'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    cell_id = sqlalchemy.Column(sqlalchemy.Integer)
    lac = sqlalchemy.Column(sqlalchemy.Integer)
    longitude = sqlalchemy.Column(sqlalchemy.Integer)
    latitude = sqlalchemy.Column(sqlalchemy.Integer)
