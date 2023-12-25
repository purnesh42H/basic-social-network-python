
# app.py

from aiohttp import web
from app.routes import setup_routes
from app.database import InMemorySocialNetworkDatabase
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.friend_service import FriendService
from app.services.chat_service import ChatService
from app.services.post_service import PostService
from app.services.timeline_service import TimelineService

async def init_app():
    app = web.Application()
    
    database = InMemorySocialNetworkDatabase()
    auth_service = AuthService(database=database)
    user_service = UserService(database=database)
    friend_service = FriendService(database=database)
    chat_service = ChatService(database=database)
    post_service = PostService(database=database,
                               user_service=user_service,
                               friend_service=friend_service)
    timeline_service = TimelineService(database=database,
                                       user_service=user_service,
                                       friend_service=friend_service)

    setup_routes(app=app,
                 auth_service=auth_service,
                 user_service=user_service,
                 friend_service=friend_service,
                 chat_service=chat_service,
                 post_service=post_service,
                 timeline_service=timeline_service)  # Function to set up routes, see below

    return app

if __name__ == '__main__':
    app = init_app()
    web.run_app(app, port=8080)
