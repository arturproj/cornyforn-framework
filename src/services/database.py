from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Base:
    """Base class for all models."""
    __abstract__ = True 

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    pass
