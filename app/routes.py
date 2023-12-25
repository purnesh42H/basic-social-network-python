# routes.py

from aiohttp import web
from app.controllers.auth_controller import AuthController
from app.controllers.user_controller import UserController
from app.controllers.friend_controller import FriendController
from app.services.auth_service import AuthService

def setup_routes(app, database, auth_service, user_service, friend_service):
    auth_controller = AuthController(auth_service=auth_service)
    user_controller = UserController(auth_service=auth_service,
                                     user_service=user_service)
    friend_controller = FriendController(auth_service=auth_service,
                                         user_service=user_service,
                                         friend_service=friend_service)

    app.router.add_post('/login', auth_controller.login)
    app.router.add_post('/register', user_controller.register)
    app.router.add_get('/get_user_id/{username}', user_controller.get_user_id)
    app.router.add_post('/add_friend', friend_controller.send_friend_request)
    app.router.add_post('/accept_friend', friend_controller.accept_friend_request)
    app.router.add_get('/friends/{user_id}', friend_controller.get_friends)