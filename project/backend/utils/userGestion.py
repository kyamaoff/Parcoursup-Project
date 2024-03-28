from flask import session
from ..models.user import User

class UserManagement:
    def __init__(self):
        self.username = None
        self.user = None

    def get_user_info(self):
        if 'username' in session:
            self.username = session['username']
            self.user = User.query.filter_by(Name=self.username).first()
        return self.username, self.user