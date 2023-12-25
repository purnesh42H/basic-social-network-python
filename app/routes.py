# routes.py

from aiohttp import web
from app.controllers.auth_controller import AuthController
from app.controllers.user_controller import UserController
from app.controllers.friend_controller import FriendController
from app.controllers.chat_controller import ChatController
from app.controllers.post_controller import PostController
from app.controllers.timeline_controller import TimelineController

def setup_routes(app, auth_service, user_service, friend_service, chat_service, post_service, timeline_service):
    auth_controller = AuthController(auth_service=auth_service)
    user_controller = UserController(auth_service=auth_service,
                                     user_service=user_service)
    friend_controller = FriendController(auth_service=auth_service,
                                         user_service=user_service,
                                         friend_service=friend_service)
    chat_controller = ChatController(auth_service=auth_service,
                                     user_service=user_service,
                                     chat_service=chat_service)
    post_controller = PostController(auth_service=auth_service,
                                     post_service=post_service)
    timeline_controller = TimelineController(auth_service=auth_service,
                                             timeline_service=timeline_service)

    app.router.add_post('/login', auth_controller.login)
    app.router.add_post('/register', user_controller.register)
    app.router.add_get('/user_id/{username}', user_controller.get_user_id)
    app.router.add_post('/add_friend', friend_controller.send_friend_request)
    app.router.add_post('/accept_friend', friend_controller.accept_friend_request)
    app.router.add_get('/friends/{user_id}', friend_controller.get_friends)
    app.router.add_post('/send_chat', chat_controller.send_chat)
    app.router.add_post('/receive_chat', chat_controller.receive_chat)
    app.router.add_get('/chats/{user_id}/{friend_id}', chat_controller.get_chat_history)
    app.router.add_post('/post', post_controller.post)
    app.router.add_post('/delete_post', post_controller.delete)
    app.router.add_get('/view_post/{user_id}/{post_id}', post_controller.view)
    app.router.add_get('/timeline/{user_id}', timeline_controller.get_timeline)