import sqlalchemy
from .db_session import SqlAlchemyBase


class Record(SqlAlchemyBase):
    __tablename__ = 'records'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    imsi = sqlalchemy.Column(sqlalchemy.Integer, )  # int imsi
    seen = sqlalchemy.PickleType()
    # [{"time": datetime.now(), "country": "", "brand": "", "operator": "", "LAC": 12345, "cell_id": ""}]
