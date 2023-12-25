import time
from app.models import User

class UserService(object):

    def __init__(self, database):
        self.database = database

    async def add_user(self, username, password, country):
        if username in self.database.username_user_id_mapping:
            return
        
        await self.database.add_user(
            User(username=username, password=password, country=country, timestamp=time.time()))
    
    async def get_user(self, user_id):
        if not await self.database.has_user(user_id):
            return None
        
        return await self.database.get_user(user_id)
    
    async def get_user_by_username(self, username):
        if username not in self.database.username_user_id_mapping:
            return None
        
        return await self.database.get_user_by_username(username)
