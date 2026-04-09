from services.database import db, Base
from datetime import datetime
from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class UserModel:
    id: Mapped[int]
    username: Mapped[str]
    password: Mapped[str]
    createdAt: Mapped[datetime]
    updatedAt: Mapped[datetime]
    deletedAt: Mapped[datetime]

class User(UserModel, Base):
    __tablename__ = 't_users'

    id: Mapped[int] = mapped_column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True
    )
    username: Mapped[str] = mapped_column(
        db.String(100),
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(
        db.String(255),
        nullable=False
    )

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

