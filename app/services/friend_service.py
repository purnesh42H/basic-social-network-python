class FriendService(object):

    def __init__(self, database):
        self.database = database
    
    def send_friend_request(self, from_user_id, to_user_id):
        to_user = self.database.get_user(user_id=to_user_id)
        to_user.pending_friend_requests.add(from_user_id)

    def accept_friend_request(self, from_user_id, to_user_id):
        to_user = self.database.get_user(user_id=to_user_id)
        from_user = self.database.get_user(user_id=from_user_id)

        from_user.friends.add(to_user_id)
        to_user.friends.add(from_user_id)
        to_user.pending_friend_requests.remove(from_user_id)

    def get_friends(self, user_id):
        user = self.database.get_user(user_id=user_id)
        return list(user.friends)
