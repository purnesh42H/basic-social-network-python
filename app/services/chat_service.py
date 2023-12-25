import time
from app.models import Chat

class ChatService(object):

    def __init__(self, database):
        self.database = database
    
    async def send_chat(self, from_user_id, to_user_id, message):
        timestamp = time.time()
        chat = Chat(from_user_id=from_user_id, to_user_id=to_user_id, timestamp=timestamp, status="SENT", message=message)
        
        await self.database.queue_chat(user_id=to_user_id, friend_id=from_user_id, chat=chat)
        await self.database.add_chat(user_id=from_user_id, friend_id=to_user_id, chat=chat)

    async def receive_chat(self, from_user_id, to_user_id):
        if not await self.database.has_unviewed_chat(user_id=to_user_id, friend_id=from_user_id) :
            return None

        chat = await self.database.dequeu_chat(user_id=to_user_id, friend_id=from_user_id)
        timestamp = time.time()
        chat.timestamp = timestamp
        chat.status = "DELIVERED"
        
        await self.database.add_chat(user_id=to_user_id, friend_id=from_user_id, chat=chat)

        return chat.id

    async def chat_history(self, user_id, friend_id):
        if not await self.database.has_chat(user_id=user_id, friend_id=friend_id):
            return {}
        
        return await self.database.get_chat_history(user_id=user_id, friend_id=friend_id)
