import uuid

class User(object):

    def __init__(self, username, password, country, timestamp):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.country = country
        self.timestamp = timestamp
        self.friends = set() # {friend_ids}
        self.posts = set() # {post_ids}
        self.pending_friend_requests = set() # {friend_ids}
        self.timeline = {} # {post_id: friend_id} top 10 post_ids

class Post(object):

    def __init__(self, owner_id, content, timestamp):
        self.id = str(uuid.uuid4())
        self.owner_id = owner_id
        self.content = content
        self.timestamp = timestamp

class Chat(object):

    def __init__(self, sender_id, receiver_id, timestamp):
        self.id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.timestamp = timestamp

class Friend(object):

    def __init__(self, user_id1, user_id2, timestamp):
        self.id = str(uuid.uuid4())
        self.user_id1 = user_id1
        self.user_id2 = user_id2
        self.timestamp = timestamp

class PendingFriendRequest(object):

    def __init__(self, from_id, to_id, timestamp):
        self.id = str(uuid.uuid4())
        self.from_id = from_id
        self.to_id = to_id
        self.timestamp = timestamp