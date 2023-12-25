# app/services/auth_service.py
import jwt

SECRET_KEY = 'your_secret_key'  # Replace with a secure secret key in production
ALGORITHM = 'HS256'

class AuthService(object):

    def __init__(self, database):
        self.database = database

    def generate_token(self, username, password):
        payload = {'username': username, 'password': password}
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        self.database.add_token(token, self.database.username_user_id_mapping[username])
        return token

    def is_valid_token(self, user_id, token):
        return user_id in self.database.users \
            and self.database.tokens[token] == user_id
    
    def validate_credentials(self, username, password):
        if username not in self.database.username_user_id_mapping:
            return False
        
        user_id = self.database.username_user_id_mapping[username]
        return user_id in self.database.users and self.database.users[user_id].password == password

