# app/services/auth_service.py
import jwt
import asyncio

SECRET_KEY = 'your_secret_key'  # Replace with a secure secret key in production
ALGORITHM = 'HS256'

class AuthService(object):

    def __init__(self, database):
        self.database = database
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(value=10)

    async def generate_token(self, username, password):
        async with self.semaphore:
            current_token = (await self.database.get_user(self.database.username_user_id_mapping[username])).token
            if current_token:
                async with self.lock:
                    await self.database.remove_token(current_token)
            
            payload = {'username': username, 'password': password}
            token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

            async with self.lock:
                await self.database.add_token(token, self.database.username_user_id_mapping[username])
            
            return token

    async def is_valid_token(self, user_id, token):
        return user_id in self.database.users \
            and self.database.tokens[token] == user_id
    
    async def validate_credentials(self, username, password):
        if username not in self.database.username_user_id_mapping:
            return False
        
        user_id = self.database.username_user_id_mapping[username]
        return user_id in self.database.users and self.database.users[user_id].password == password

