from services.database import db, Base
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import event


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

# Optional: event to set updatedAt on update
# This will automatically set the updatedAt field to the current time
# Alternatively, you can use the `onupdate` parameter in the Column definition
# Also, you can use the trigger sql to set the updatedAt field 
@event.listens_for(Example, 'before_update')
def soft_update(mapper, connection, target):
    connection.execute(
        Example.__table__.update()
        .where(Example.id == target.id)
        .values(updatedAt=func.now())
    )

# Optional: event to set deletedAt to "soft delete"
@event.listens_for(Example, 'before_delete')
def soft_delete(mapper, connection, target):
    # Prevents physical deletion
    if target.deletedAt is None:
        connection.execute(
            Example.__table__.update()
            .where(Example.id == target.id)
            .values(deletedAt=func.now())
        )
    else:
        raise Exception(
            "Soft delete only: the record was not physically deleted")
