# app/controllers/auth_controller.py
import jwt
from aiohttp import web

class AuthController(object):
    def __init__(self, auth_service):
        self.auth_service = auth_service

    async def login(self, request):
        data = await request.post()
        username = data.get('username')
        password = data.get('password')

        if self.validate_credentials(username, password):
            token = self.generate_token(username, password)
            return web.json_response({'token': token})
        else:
            return web.Response(status=401, text='Invalid credentials')

    def validate_credentials(self, username, password):
        return self.auth_services.validate_credentials(username=username, password=password)

    def generate_token(self, username, password):
        return self.auth_service.generate_token(username=username, password=password)

