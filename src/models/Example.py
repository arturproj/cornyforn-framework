from services.database import db, Base
from datetime import datetime
from sqlalchemy.sql import func

class Example(db.Model, Base):
    id: int
    message: str
    createdAt: datetime
    updatedAt: datetime
    deletedAt: datetime

    __tablename__ = 't_examples'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False,
                   unique=True)
    message = db.Column(db.Text)

    createdAt = db.Column(db.DateTime, nullable=False,
                          default=func.now())
    updatedAt = db.Column(db.DateTime, nullable=True,
                          default=None, onupdate=func.now())
    deletedAt = db.Column(db.DateTime, nullable=True,
                          default=None)

