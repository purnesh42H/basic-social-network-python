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
    
    def send_friend_request(self, to_user_id):
        url = f"{self.base_url}/add_friend"
        payload = {'from_user_id': self.user_id, 'to_user_id': to_user_id}
        return requests.post(url, data=payload, headers=self.headers)
    
    def accept_friend_request(self, from_user_id):
        url = f"{self.base_url}/accept_friend"
        payload = {'from_user_id': from_user_id, 'to_user_id': self.user_id}
        return requests.post(url, data=payload, headers=self.headers)

    def get_user_id(self):
        url = f"{self.base_url}/get_user_id/{self.username}"
        return requests.get(url, headers=self.headers)
    
    def get_friends(self):
        url = f"{self.base_url}/friends/{self.user_id}"
        return requests.get(url, headers=self.headers)
    
    def set_token(self, token):
        self.headers['Authorization'] = f'Bearer {token}'

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_username(self, username):
        self.username = username

def test_social_network():
    base_url = "http://localhost:8080"
    
    user_1_client = TestClient(base_url)
    user_2_client = TestClient(base_url)

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

if __name__ == '__main__':
    test_social_network()
