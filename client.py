import requests
import json
from time import time

# GET request test
# req = requests.get('http://localhost:5000/ping')
# print(req.json())

# POST request test
req = requests.post('http://localhost:5000/login', json={'name':'thbop', 'password':'Beef64'})
print(req.json())


# req_concept = {
#     'key': 'testkey', # Test user key, would normally be a random string of characters. This is used to tell the server which user is making the request.
#     'action': 'send-message', # Defines what the user would like the server to do. 
#     'data': {'message': 'test message'} # Based on what the user asked, we may need to send some extra data such as the message contents.
# }
# 
# This is a concept request that would be sent to the server.
# The chat "server" and chat "channel" would be defined by POSTing this request to the url /server_id/channel_id
# Both ids will be a random string of characters for security purposes.

class Client:
    def __init__(self):
        self.load_data()

    def load_data(self):
        base_data = {
            'url':'http://localhost:5000',
            'key': None
        }
        try:
            file = open('client-data.json')
            self.data = json.load(file)
            file.close()
        except FileNotFoundError:
            file = open('client-data.json', 'w')
            file.write(
                json.dumps(base_data)
            )
            file.close()
            self.data = base_data
    
    def save_data(self):
        file = open('client-data.json', 'w')
        file.write(
            json.dumps(self.data)
        )
        file.close()
    
    def ping(self):
        req = requests.get(self.data['url'] + '/ping')
        return req.json()

if __name__ == '__main__':
    client = Client()