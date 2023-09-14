# models.py

from risk_assessment_db import get_user_by_id, get_user_by_username
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password_hash = password

    @staticmethod
    def get(user_id):
        user_data = get_user_by_id(user_id)
        if user_data:
            return User(user_data[0], user_data[1], user_data[2])
        return None

    @staticmethod
    def get_by_username(username):
        user_data = get_user_by_username(username)
        if user_data:
            return User(user_data[0], user_data[1], user_data[2])
        return None
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
