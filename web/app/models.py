from flask_login import UserMixin
from app import db

# UserMixin includes generic attributes that will be used for sessions
# This includes:
# - Session token: needed for authentication in the API
# - User id: will be used for some actions such as showing the profile of the user that is
# logged in.
class User(UserMixin, db.Model):
    # This is the row id of the sessions table inside Flask, not the one used in the API
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    user_id = db.Column(db.Integer)
    token = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Get functions, in order to get data of the logged-in user to pass it to the API use:
    # - current_user.funtion()
    def get_username(self):
        return self.username

    def get_userid(self):
        return self.user_id

    def get_token(self):
        return self.token
