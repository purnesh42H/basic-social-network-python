class TimelineService(object):

    def __init__(self, database, user_service, friend_service):
        self.database = database
        self.user_service = user_service
        self.friend_service = friend_service

    async def get_timeline(self, user_id):
        user = await self.user_service.get_user(user_id)
        return user.timeline