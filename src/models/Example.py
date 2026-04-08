from services.database import db, Base
from datetime import datetime
from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class ExampleModel:
    id: Mapped[int]
    message: Mapped[str]
    createdAt: Mapped[datetime]
    updatedAt: Mapped[datetime]
    deletedAt: Mapped[datetime]

class Example(ExampleModel, Base):
    __tablename__ = 't_examples'

    id: Mapped[int] = mapped_column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True
    )
    message: Mapped[str] = mapped_column(db.Text)

    createdAt: Mapped[datetime] = mapped_column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )
    updatedAt: Mapped[datetime] = mapped_column(
        db.DateTime,
        nullable=True,
        default=None,
        onupdate=func.now()
    )
    deletedAt: Mapped[datetime] = mapped_column(
        db.DateTime,
        nullable=True,
        default=None
    )

