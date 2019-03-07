from flask_login import UserMixin
from app import db

# UserMixin includes generic attributes that will be used for sessions
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
