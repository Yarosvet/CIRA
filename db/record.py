import sqlalchemy
from .db_session import SqlAlchemyBase


class Record(SqlAlchemyBase):
    __tablename__ = 'records'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    imsi = sqlalchemy.Column(sqlalchemy.Integer)  # int imsi
    country = sqlalchemy.Column(sqlalchemy.String)
    brand = sqlalchemy.Column(sqlalchemy.String)
    operator = sqlalchemy.Column(sqlalchemy.String)
    seen = sqlalchemy.Column(sqlalchemy.PickleType)
    # [{"timestamp": datetime.now(), "LAC": 12345, "cell_id": ""}]
    phone_number = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String)
    log_level = sqlalchemy.Column(sqlalchemy.Integer)
