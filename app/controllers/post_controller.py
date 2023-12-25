# app/controllers/post_controller.py
from aiohttp import web
import app.utils
from datetime import datetime

class PostController(object):
    
    def __init__(self, auth_service, post_service):
        self.auth_service = auth_service
        self.post_service = post_service

    async def post(self, request):
        data = await request.post()
        
        token = app.utils.get_token(request=request)
        user_id = data.get('user_id')
        if not token or not (await self.auth_service.is_valid_token(user_id=user_id, token=token)):
            return web.Response(status=401, text='User not authorized')
        
        user = await self.post_service.user_service.get_user(user_id=user_id)
        if not user:
            return web.Response(status=404, text='User not found')
        
        content = data.get('content')
        post_id = await self.post_service.post(user_id=user_id, content=content)
        return web.json_response({'post_id': post_id})
    
    async def delete(self, request):
        data = await request.post()

        token = app.utils.get_token(request=request)
        user_id = data.get('user_id')
        if not token or not (await self.auth_service.is_valid_token(user_id=user_id, token=token)):
            return web.Response(status=401, text='User not authorized')
        
        user = await self.post_service.user_service.get_user(user_id=user_id)
        if not user:
            return web.Response(status=404, text='User not found')
        
        post_id = data.get('post_id')
        await self.post_service.delete(user_id=user_id, post_id=post_id)
        return web.Response(status=200, text='Post deleted')
    
    async def view(self, request):
        token = app.utils.get_token(request=request)
        requestor_id = app.utils.get_requestor_id(request=request)
        if not token or not (await self.auth_service.is_valid_token(user_id=requestor_id, token=token)):
            return web.Response(status=401, text='User not authorized')

        user_id = request.match_info['user_id']
        user = await self.post_service.user_service.get_user(user_id=user_id)
        if not user:
            return web.Response(status=404, text='Poster not found')
        
        post_id = request.match_info['post_id']
        post = await self.post_service.view(user_id=user_id, post_id=post_id)
        if not post:
            return web.Response(status=404, text='Post not found')

        return web.json_response({'post': [str(datetime.fromtimestamp(post.timestamp)), post.user_id, post.content]})

