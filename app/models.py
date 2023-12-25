import uuid
from collections import defaultdict, deque, OrderedDict

class User(object):

    def __init__(self, username, password, country, timestamp):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.country = country
        self.timestamp = timestamp
        self.token = None
        self.chat_history = defaultdict(list) # {friend_id: [Chat()]}
        self.chat_queue = defaultdict(deque) # {friend_id: deque()}
        self.friends = {} # {friend_id: Friend()}
        self.posts = {} # {post_id: Post()}
        self.pending_friend_requests = {} # {friend_id: Friend()}
        self.timeline = OrderedDict() # {post_id: {friend_username, snippet}} top 10 post_ids

class Post(object):

    def __init__(self, user_id, content, timestamp):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.content = content
        self.snippet = content[:50]
        self.timestamp = timestamp

class Chat(object):

    def __init__(self, from_user_id, to_user_id, timestamp, status, message):
        self.id = str(uuid.uuid4())
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.status = status # SENT, DELIVERED
        self.timestamp = timestamp
        self.message = message

class Friend(object):

    def __init__(self, from_user_id, to_user_id, timestamp, status):
        self.id = str(uuid.uuid4())
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.status = status # FRIEND, PENDING
        self.timestamp = timestamp
