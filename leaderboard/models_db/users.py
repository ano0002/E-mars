from datetime import datetime
from data import db
import sys

sys.path.append("../")


class user(db.Model):
    """
    Initiating the users table in python
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(63), unique=True, nullable=False)
    level = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f'<name - {self.name}>'
