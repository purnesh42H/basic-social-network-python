# app/controllers/timeline_controller.py
from aiohttp import web
import app.utils
from datetime import datetime

class TimelineController(object):

    def __init__(self, auth_service, timeline_service):
        self.auth_service = auth_service
        self.timeline_service = timeline_service

    async def get_timeline(self, request):
        token = app.utils.get_token(request=request)
        user_id = request.match_info['user_id']
        if not token or not (await self.auth_service.is_valid_token(user_id=user_id, token=token)):
            return web.Response(status=401, text='User not authorized')

        user = await self.timeline_service.user_service.get_user(user_id=user_id)
        if not user:
            return web.Response(status=404, text='User not found')
        
        timeline = await self.timeline_service.get_timeline(user_id=user_id)
        timeline_view = []
        for _, (friend_id, snippet) in reversed(timeline.items()):
            timeline_view.append([friend_id, snippet])

        return web.json_response({'timeline': timeline_view})  
