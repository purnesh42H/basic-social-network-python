import time
import asyncio
from app.models import Post

POPULAR_USER_THRSHOLD = 5000
TIMELINE_THRESHOLD = 1

class PostService(object):

    def __init__(self, database, user_service, friend_service):
        self.database = database
        self.user_service = user_service
        self.friend_service = friend_service
        self.semaphore = asyncio.Semaphore(value=10)
        self.lock = asyncio.Lock()
    
    async def post(self, user_id, content):
        timestamp = time.time()
        post = Post(user_id=user_id, content=content, timestamp=timestamp)
        
        async with self.semaphore:
            user = await self.user_service.get_user(user_id)
            user.posts[post.id] = post

            friends = await self.friend_service.get_friends(user_id=user_id)
            if len(friends) < POPULAR_USER_THRSHOLD:
                for friend_id, friend in friends.items():
                    async with self.lock:
                        friend = await self.user_service.get_user(friend_id)
                        friend.timeline[post.id] = (post.user_id, post.snippet)
                        if len(friend.timeline) > TIMELINE_THRESHOLD:
                            friend.timeline.popitem(last=False)

            return post.id

    async def view(self, user_id, post_id):
        async with self.semaphore:
            user = await self.user_service.get_user(user_id)
            if post_id not in user.posts:
                return None
            
            return user.posts[post_id]

    async def delete(self, user_id, post_id):
        async with self.semaphore:
            user = await self.user_service.get_user(user_id=user_id)
            if post_id not in user.posts:
                return

            del user.posts[post_id]

            friends = await self.friend_service.get_friends(user_id=user_id)
            if len(friends) < POPULAR_USER_THRSHOLD:
                for friend_id, friend in friends.items():
                    async with self.lock:
                        friend = await self.user_service.get_user(friend_id)
                        del friend.timeline[post_id]
