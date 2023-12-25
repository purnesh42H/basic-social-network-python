# app/controllers/user_controller.py
from aiohttp import web
import app.utils

class UserController(object):
    
    def __init__(self, user_service, auth_service):
        self.auth_service = auth_service
        self.user_service = user_service

    async def register(self, request):
        data = await request.post()
        username = data.get('username')
        password = data.get('password')
        country = data.get('country')

        if await self.user_service.get_user_by_username(username=username):
            return web.Response(status=400, text='Username already exist')

        await self.user_service.add_user(username=username, password=password, country=country)
        token = await self.auth_service.generate_token(username=username, password=password)

        return web.json_response({'token': token})
    
    async def get_user_id(self, request):    
        username = request.match_info['username']
        user = await self.user_service.get_user_by_username(username)
        if not user:
            return web.Response(status=404, text='Username not found')
        
        token = app.utils.get_token(request=request)
        if not token or not (await self.auth_service.is_valid_token(user_id=user.id, token=token)):
            return web.Response(status=401, text='User not authorized')
        
        return web.json_response({'user_id': user.id}) 
