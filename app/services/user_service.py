import time
import asyncio
from app.models import User

class UserService(object):

    def __init__(self, database):
        self.database = database
        self.semaphore = asyncio.Semaphore(value=10)

    async def add_user(self, username, password, country):
        async with self.semaphore:
            if username in self.database.username_user_id_mapping:
                return
        
            await self.database.add_user(
                User(username=username, password=password, country=country, timestamp=time.time()))
    
    async def get_user(self, user_id):
        async with self.semaphore:
            if not await self.database.has_user(user_id):
                return None
            
            return await self.database.get_user(user_id)
    
    async def get_user_by_username(self, username):
        async with self.semaphore:
            if username not in self.database.username_user_id_mapping:
                return None
            
            return await self.database.get_user_by_username(username)
