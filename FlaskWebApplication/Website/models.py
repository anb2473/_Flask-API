from . import db
from flask_login import UserMixin

from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # sql naturally references functions by lowercase,
    # so User is represented as user
    # foriegn key only works for a many-to-one relationship
    # (many notes to one user)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    # sql requires a capitol for the relationship field
    notes = db.relationship('Note')
