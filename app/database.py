# app/database.py
class InMemorySocialNetworkDatabase(object):
    
    def __init__(self):
        self.users = {}
        self.username_user_id_mapping = {}
        self.tokens = {}
        self.posts = {}
        self.chats = {}

    def add_user(self, user):
        self.users[user.id] = user
        self.username_user_id_mapping[user.username] = user.id
        print(self.username_user_id_mapping)

    def has_user(self, user_id):
        return user_id in self.users

    def get_user(self, user_id):
        return self.users[user_id]

    def add_token(self, token, user_id):
        self.tokens[token] = user_id

    def get_user_by_username(self, username):
        user_id = self.username_user_id_mapping[username]
        return self.users[user_id]
