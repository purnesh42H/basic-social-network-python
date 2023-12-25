# app/controllers/friend_controller.py
from aiohttp import web
import time
from app.models import User, Friend
import app.utils

class FriendController(object):
    
    def __init__(self, auth_service, user_service, friend_service):
        self.user_service = user_service
        self.auth_service = auth_service
        self.user_service = user_service
        self.friend_service = friend_service

    async def send_friend_request(self, request):
        data = await request.post()
        
        token = app.utils.get_token(request=request)
        from_user_id = data.get('from_user_id')
        if not token or not self.auth_service.is_valid_token(user_id=from_user_id, token=token):
            return web.Response(status=401, text='User not authorized')

        to_user_id = data.get('to_user_id')

        from_user = self.user_service.get_user(user_id=from_user_id)
        if not from_user:
            return web.Response(status=404, text='Requestor not found')
            
        to_user = self.user_service.get_user(user_id=to_user_id)
        if not to_user:
            return web.Response(status=404, text='Friend not found')
        
        self.friend_service.send_friend_request(from_user_id=from_user_id, to_user_id=to_user_id)
        return web.Response(status=200, text='Friend Request Sent to ' + to_user.username)
    
    async def accept_friend_request(self, request):
        data = await request.post()

        token = app.utils.get_token(request=request)
        to_user_id = data.get('to_user_id')
        if not token or not self.auth_service.is_valid_token(user_id=to_user_id, token=token):
            return web.Response(status=401, text='User not authorized')
        
        from_user_id = data.get('from_user_id')

        from_user = self.user_service.get_user(user_id=from_user_id)
        if not from_user:
            return web.Response(status=404, text='Requestor not found')
            
        to_user = self.user_service.get_user(user_id=to_user_id)
        if not to_user:
            return web.Response(status=404, text='User not found')
        
        self.friend_service.accept_friend_request(from_user_id=from_user_id, to_user_id=to_user_id)
        return web.Response(status=200, text='Friend Added ' + from_user.username)
    
    async def get_friends(self, request):        
        token = app.utils.get_token(request=request)
        user_id = request.match_info['user_id']
        if not token or not self.auth_service.is_valid_token(user_id=user_id, token=token):
            return web.Response(status=401, text='User not authorized')

        user = self.user_service.get_user(user_id=user_id)
        if not user:
            return web.Response(status=404, text='User not found')
        
        friends = self.friend_service.get_friends(user_id)
        friend_usernames = []
        for friend_id in friends:
            friend_usernames.append(self.user_service.get_user(friend_id).username)

        return web.json_response({'friends': friend_usernames})

