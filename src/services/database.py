from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Base:
    """Base class for all models."""
    __abstract__ = True 

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def to_dict(self):
        """Convert the Example instance to a dictionary."""
        return {
            'id': self.id,
            'message': self.message,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None,
            'deletedAt': self.deletedAt.isoformat() if self.deletedAt else None
        }

    pass
