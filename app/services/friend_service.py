import time
import asyncio
from app.models import Friend

class FriendService(object):

    def __init__(self, database):
        self.database = database
        self.semaphore = asyncio.Semaphore(value=10)
    
    async def send_friend_request(self, from_user_id, to_user_id):
        timestamp = timestamp=time.time()
        friend = Friend(from_user_id=from_user_id, to_user_id=to_user_id, timestamp=timestamp, status="PENDING")
        
        await self.database.add_pending_friend(user_id=to_user_id, friend_id=from_user_id, friend=friend)
        await self.database.add_pending_friend(user_id=from_user_id, friend_id=to_user_id, friend=friend)

    async def accept_friend_request(self, from_user_id, to_user_id):
        timestamp = timestamp=time.time()

        friend = await self.database.get_pending_friend(user_id=to_user_id, friend_id=from_user_id)
        friend.status = "FRIEND"
        friend.timestamp = timestamp
        
        await self.database.remove_pending_friend(user_id=to_user_id, friend_id=from_user_id)
        await self.database.add_friend(user_id=to_user_id, friend_id=from_user_id, friend=friend)

        await self.database.remove_pending_friend(user_id=from_user_id, friend_id=to_user_id)
        await self.database.add_friend(user_id=from_user_id, friend_id=to_user_id, friend=friend)

    async def get_friends(self, user_id):
        return await self.database.get_all_friends(user_id=user_id)
