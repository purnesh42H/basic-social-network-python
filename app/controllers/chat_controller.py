# app/controllers/chat_controller.py
from aiohttp import web
import app.utils
from datetime import datetime

class ChatController(object):
    
    def __init__(self, auth_service, user_service, chat_service):
        self.auth_service = auth_service
        self.user_service = user_service
        self.chat_service = chat_service

    async def send_chat(self, request):
        data = await request.post()
        
        token = app.utils.get_token(request=request)
        from_user_id = data.get('from_user_id')
        if not token or not (await self.auth_service.is_valid_token(user_id=from_user_id, token=token)):
            return web.Response(status=401, text='User not authorized')

        to_user_id = data.get('to_user_id')

        from_user = await self.user_service.get_user(user_id=from_user_id)
        if not from_user:
            return web.Response(status=404, text='Requestor not found')
            
        to_user = await self.user_service.get_user(user_id=to_user_id)
        if not to_user:
            return web.Response(status=404, text='Friend not found')
        
        message = data.get('message')
        await self.chat_service.send_chat(from_user_id=from_user_id, to_user_id=to_user_id, message=message)
        return web.Response(status=200, text='Chat Sent to ' + to_user.username)
    
    async def receive_chat(self, request):
        data = await request.post()

        token = app.utils.get_token(request=request)
        to_user_id = data.get('to_user_id')
        if not token or not (await self.auth_service.is_valid_token(user_id=to_user_id, token=token)):
            return web.Response(status=401, text='User not authorized')
        
        from_user_id = data.get('from_user_id')

        from_user = await self.user_service.get_user(user_id=from_user_id)
        if not from_user:
            return web.Response(status=404, text='Requestor not found')
            
        to_user = await self.user_service.get_user(user_id=to_user_id)
        if not to_user:
            return web.Response(status=404, text='User not found')
        
        chat_id = await self.chat_service.receive_chat(from_user_id=from_user_id, to_user_id=to_user_id)
        if not chat_id:
            return web.Response(status=400, text='No chats available ' + from_user.username)
        
        return web.Response(status=200, text='Chat Recieved from ' + from_user.username)
    
    async def get_chat_history(self, request):        
        token = app.utils.get_token(request=request)
        user_id = request.match_info['user_id']
        if not token or not (await self.auth_service.is_valid_token(user_id=user_id, token=token)):
            return web.Response(status=401, text='User not authorized')

        user = await self.user_service.get_user(user_id=user_id)
        if not user:
            return web.Response(status=404, text='User not found')
        
        friend_id = request.match_info['friend_id']
        chats = await self.chat_service.chat_history(user_id=user_id, friend_id=friend_id)
        chat_messages = []
        for chat in chats:
            direction = "RECEIVED"
            if chat.from_user_id == user_id:
                direction = "SENT"
            
            chat_messages.append([str(datetime.fromtimestamp(chat.timestamp)), direction, str(chat.status), chat.message])

        return web.json_response({'chats': chat_messages})

