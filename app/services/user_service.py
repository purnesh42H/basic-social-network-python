class UserService(object):

    def __init__(self, database):
        self.database = database

    def add_user(self, user):
        if user.id in self.database.users:
            return
        
        self.database.add_user(user)
    
    def get_user(self, user_id):
        if not self.database.has_user(user_id):
            return None
        
        return self.database.get_user(user_id)
    
    def get_user_by_username(self, username):
        if username not in self.database.username_user_id_mapping:
            return None
        
        return self.database.get_user_by_username(username)
