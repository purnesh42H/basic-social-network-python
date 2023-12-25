# app/database.py
import asyncio

class InMemorySocialNetworkDatabase(object):
    
    def __init__(self):
        self.users = {}
        self.username_user_id_mapping = {}
        self.tokens = {}
        self.lock = asyncio.Lock()

    async def add_token(self, token, user_id):
        async with self.lock:
            self.tokens[token] = user_id
            (await self.get_user(user_id=user_id)).token = token

    async def remove_token(self, token):
        async with self.lock:
            del self.tokens[token]
    
    async def add_user(self, user):
        async with self.lock:
            self.users[user.id] = user
            self.username_user_id_mapping[user.username] = user.id
    
    async def add_pending_friend(self, user_id, friend_id, friend):
        user = await self.get_user(user_id=user_id)
        async with self.lock:
            user.pending_friend_requests[friend_id] = friend

    async def remove_pending_friend(self, user_id, friend_id):
        user = await self.get_user(user_id=user_id)
        async with self.lock:
            del user.pending_friend_requests[friend_id]

    async def add_friend(self, user_id, friend_id, friend):
        user = await self.get_user(user_id=user_id)
        async with self.lock:
            user.friends[friend_id] = friend

    async def queue_chat(self, user_id, friend_id, chat):
        user = await self.get_user(user_id=user_id)
        async with self.lock:
            user.chat_queue[friend_id].append(chat)

    async def add_chat(self, user_id, friend_id, chat):
        user = await self.get_user(user_id=user_id)
        async with self.lock:
            user.chat_history[friend_id].append(chat)

    async def dequeu_chat(self, user_id, friend_id):
        user = await self.get_user(user_id=user_id)
        async with self.lock:
            return user.chat_queue[friend_id].popleft()

    async def has_user(self, user_id):
        return user_id in self.users

    async def get_user(self, user_id):
        return self.users[user_id]

    async def get_user_by_username(self, username):
        user_id = self.username_user_id_mapping[username]
        return self.users[user_id]
    
    async def get_pending_friend(self, user_id, friend_id):
        user = await self.get_user(user_id=user_id)
        return user.pending_friend_requests[friend_id]
    
    async def get_all_friends(self, user_id):
        user = await self.get_user(user_id=user_id)
        return user.friends
    
    async def has_unviewed_chat(self, user_id, friend_id):
        user = await self.get_user(user_id=user_id)
        return user.chat_queue[friend_id] is not None
    
    async def has_chat(self, user_id, friend_id):
        user = await self.get_user(user_id=user_id)
        return user.chat_history[friend_id] is not None
    
    async def get_chat_history(self, user_id, friend_id):
        user = await self.get_user(user_id=user_id)
        return user.chat_history[friend_id]
