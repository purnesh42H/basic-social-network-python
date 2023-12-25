# tests/clients/social_network.py
import requests

''''
Example Usecase
- User 1 and User 2 registers
- User 1 send friend request to User 2
- User 2 accept friend request and send message to User 1
- User 3 registers and become friend with User 2
- User 1 posts
- User 2 posts
- User 3 see timeline of User 1 recent post
'''

'''
curl -X POST -d "username=user_2&password=password_2&country=country_2" http://localhost:8080/register
curl -X POST -d "username=user_1&password=password_1&country=country_1" http://localhost:8080/register

User 1
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJfMSIsInBhc3N3b3JkIjoicGFzc3dvcmRfMSJ9.zNAaALirXEpaHhspFjD6GTsbrVLpahuDxebUgOZyngo" http://localhost:8080/get_user_id/user_1
{"user_id": "3ab2ff95-dd35-4ae3-b1e4-a4e11654598e"}

User 2
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJfMiIsInBhc3N3b3JkIjoicGFzc3dvcmRfMiJ9.es_YRcUusEw4xFxYcFm6VQURwVSyjod6oAjCM0AOCyk" http://localhost:8080/get_user_id/user_2
{"user_id": "c8475d9e-62f9-42e2-ae2f-553b82d61836"}

curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJfMSIsInBhc3N3b3JkIjoicGFzc3dvcmRfMSJ9.zNAaALirXEpaHhspFjD6GTsbrVLpahuDxebUgOZyngo" -d "from_user_id=3ab2ff95-dd35-4ae3-b1e4-a4e11654598e&to_user_id=c8475d9e-62f9-42e2-ae2f-553b82d61836" http://localhost:8080/add_friend
curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJfMiIsInBhc3N3b3JkIjoicGFzc3dvcmRfMiJ9.es_YRcUusEw4xFxYcFm6VQURwVSyjod6oAjCM0AOCyk" -d "from_user_id=3ab2ff95-dd35-4ae3-b1e4-a4e11654598e&to_user_id=c8475d9e-62f9-42e2-ae2f-553b82d61836" http://localhost:8080/accept_friend

curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJfMiIsInBhc3N3b3JkIjoicGFzc3dvcmRfMiJ9.es_YRcUusEw4xFxYcFm6VQURwVSyjod6oAjCM0AOCyk" http://localhost:8080/friends/c8475d9e-62f9-42e2-ae2f-553b82d61836
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJfMSIsInBhc3N3b3JkIjoicGFzc3dvcmRfMSJ9.zNAaALirXEpaHhspFjD6GTsbrVLpahuDxebUgOZyngo" http://localhost:8080/friends/3ab2ff95-dd35-4ae3-b1e4-a4e11654598e
'''

class TestClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {}
        self.user_id = None
        self.username = None
    
    def register(self, username, password, country):
        url = f"{self.base_url}/register"
        payload = {'username': username, 'password': password, 'country': country}
        return requests.post(url, data=payload)
    
    def login(self, username, password):
        url = f"{self.base_url}/login"
        payload = {'username': username, 'password': password}
        return requests.post(url, data=payload)
    
    def send_friend_request(self, to_user_id):
        url = f"{self.base_url}/add_friend"
        payload = {'from_user_id': self.user_id, 'to_user_id': to_user_id}
        return requests.post(url, data=payload, headers=self.headers)
    
    def accept_friend_request(self, from_user_id):
        url = f"{self.base_url}/accept_friend"
        payload = {'from_user_id': from_user_id, 'to_user_id': self.user_id}
        return requests.post(url, data=payload, headers=self.headers)
    
    def send_chat(self, to_user_id, message):
        url = f"{self.base_url}/send_chat"
        payload = {'from_user_id': self.user_id, 'to_user_id': to_user_id, 'message': message}
        return requests.post(url, data=payload, headers=self.headers)
    
    def receive_chat(self, from_user_id):
        url = f"{self.base_url}/receive_chat"
        payload = {'from_user_id': from_user_id, 'to_user_id': self.user_id}
        return requests.post(url, data=payload, headers=self.headers)
    
    def post(self, content):
        url = f"{self.base_url}/post"
        payload = {'user_id': self.user_id, 'content': content}
        return requests.post(url, data=payload, headers=self.headers)
    
    def delete_post(self, post_id):
        url = f"{self.base_url}/delete_post"
        payload = {'user_id': self.user_id, 'post_id': post_id}
        return requests.post(url, data=payload, headers=self.headers)

    def get_user_id(self):
        url = f"{self.base_url}/user_id/{self.username}"
        return requests.get(url, headers=self.headers)
    
    def get_friends(self):
        url = f"{self.base_url}/friends/{self.user_id}"
        return requests.get(url, headers=self.headers)
    
    def get_chats(self, friend_id):
        url = f"{self.base_url}/chats/{self.user_id}/{friend_id}"
        return requests.get(url, headers=self.headers)
    
    def view_post(self, user_id, post_id):
        headers = self.headers
        headers["requestor_id"] = self.user_id
        url = f"{self.base_url}/view_post/{user_id}/{post_id}"
        return requests.get(url, headers=headers)
    
    def get_timeline(self):
        url = f"{self.base_url}/timeline/{self.user_id}"
        return requests.get(url, headers=self.headers)
    
    def set_token(self, token):
        self.headers['Authorization'] = f'Bearer {token}'

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_username(self, username):
        self.username = username

def test_create_users():
    print("##user_1 REGISTERS##")
    response = user_1_client.register("user_1", "password_1", "country_1")
    data = response.json()
    print(data)
    user_1_client.set_username("user_1")
    user_1_client.set_token(data["token"])
    response = user_1_client.get_user_id()
    data = response.json()
    print(data)
    user_1_client.set_user_id(data["user_id"])

    print("\n##user_2 REGISTERS##\n")
    response = user_2_client.register("user_2", "password_2", "country_2")
    data = response.json()
    print(data)
    user_2_client.set_username("user_2")
    user_2_client.set_token(data["token"])
    response = user_2_client.get_user_id()
    data = response.json()
    print(data)
    user_2_client.set_user_id(data["user_id"])

def test_login():
    print("##user_1 LOGIN##")
    response = user_1_client.login("user_1", "password_1")
    data = response.json()
    print(data)
    user_1_client.set_username("user_1")
    user_1_client.set_token(data["token"])
    response = user_1_client.get_user_id()
    data = response.json()
    print(data)
    user_1_client.set_user_id(data["user_id"])

    print("\n##user_2 LOGIN##\n")
    response = user_2_client.login("user_2", "password_2")
    data = response.json()
    print(data)
    user_2_client.set_username("user_2")
    user_2_client.set_token(data["token"])
    response = user_2_client.get_user_id()
    data = response.json()
    print(data)
    user_2_client.set_user_id(data["user_id"])

def test_create_friends():
    print("\n##user_1 and user_2 FRIENDS##\n")
    response = user_1_client.send_friend_request(user_2_client.user_id)
    print(response.content)
    response = user_2_client.accept_friend_request(user_1_client.user_id)
    print(response.content)
    response = user_1_client.get_friends()
    data = response.json()
    print("user_1 friends {}", data)
    response = user_2_client.get_friends()
    data = response.json()
    print("user_2 friends {}", data)

def test_chats():
    print("\n##user_1 and user_2 Chats##\n")
    response = user_1_client.send_chat(user_2_client.user_id, "Hi, I am user_1")
    print(response.content)
    response = user_2_client.receive_chat(user_1_client.user_id)
    print(response.content)
    response = user_1_client.get_chats(user_2_client.user_id)
    data = response.json()
    print("user_1 chats with user_2 {}", data)
    response = user_2_client.get_chats(user_1_client.user_id)
    data = response.json()
    print("user_2 chats with user_1 {}", data)
    response = user_2_client.send_chat(user_1_client.user_id, "Hi, I am user_2. Nice to meet you")
    print(response.content)
    response = user_1_client.receive_chat(user_2_client.user_id)
    print(response.content)
    response = user_1_client.get_chats(user_2_client.user_id)
    data = response.json()
    print("user_1 chats with user_2 {}", data)
    response = user_2_client.get_chats(user_1_client.user_id)
    data = response.json()
    print("user_2 chats with user_1 {}", data)

def test_post():
    print("\n##user_1 POST##\n")
    response = user_1_client.post("I am user_1. I just joined social network")
    data = response.json()
    post_id = data['post_id']
    response = user_1_client.view_post(user_1_client.user_id, post_id)
    data = response.json()
    print("user_1 view my post {}", data)
    response = user_2_client.view_post(user_1_client.user_id, post_id)
    data = response.json()
    print("user_2 view user_1 post {}", data)
    response = user_1_client.delete_post(post_id)
    print("user_1 delete post {}", response)
    response = user_2_client.view_post(user_1_client.user_id, post_id)
    print("user_2 view user_1 post {}", response)

def test_timeline():
    print("\n##user_1 timeline##\n")
    user_2_client.post("I am user_2. Just Joined")
    response = user_1_client.get_timeline()
    data = response.json()
    print("user_1 timeline {}", data)
    user_2_client.post("I am user_2. My Second Post")
    response = user_1_client.get_timeline()
    data = response.json()
    print("user_1 timeline {}", data)

def test_social_network():
    test_create_users()
    test_login()
    test_create_friends()
    test_chats()
    test_post()
    test_timeline()

base_url = "http://localhost:8080"
user_1_client = TestClient(base_url)
user_2_client = TestClient(base_url)
    
if __name__ == '__main__':
    test_social_network()
