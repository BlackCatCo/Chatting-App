import requests
import json
from time import time


class Client:
    def __init__(self):
        '''
        The Client class manages user data and handles POST/GET requests.

        It provides simple and advanced methods for contacting the server
        such as (but not limited to) ping, login, and send_message. After
        logins/signups it will also automatically save the user's auth key
        within the "client-data.json" file.
        '''
        self.load_data()

    def load_data(self):
        '''Loads client data from the local: "client-data.json"'''
        base_data = {
            'url':'http://localhost:5000',
            'key': None,
            'cache': {
                'known-chats': []
            }
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
        '''Saves client data from the local: "client-data.json"'''
        file = open('client-data.json', 'w')
        file.write(
            json.dumps(self.data)
        )
        file.close()

    def add_known_chat(self, chat_id):
        '''[Might soon be deprecated] Adds a new known chat to the user cache.'''
        self.data['cache']['known-chats'].append(chat_id)
        self.save_data()
    
    def get_known_chats(self):
        '''[Might soon be deprecated] Gets all known chats from the user cache.'''
        return self.data['cache']['known-chats']
    
    def remove_known_chat(self, chat_id):
        '''[Might soon be deprecated] Removes a known chat from the user cache.'''
        try:
            self.data['cache']['known-chats'].remove(chat_id)
            self.save_data()
        except ValueError: pass
    
    
    def ping(self):
        '''
        Sends a quick ping to the server.
        It will return a 1 if the server responded, a 0 otherwise.
        '''
        try:
            req = requests.get(self.data['url'] + '/ping')
            out = req.json()
        except requests.exceptions.ConnectionError:
            out = 0
        return out

    def send_req_raw(self, eurl, data):
        '''
        POSTs any json to the extended url
        (baseurl.com/extended/url)

        It will return a 1 if the server responded, a 0 otherwise.
        '''
        try:
            req = requests.post(self.data['url'] + eurl , json=data)
            out = req.json()
        except requests.exceptions.ConnectionError:
            out = 0
        return out
    
    def login(self, name, password):
        '''
        Logs in to the server using the given username and password.
        If there are no errors, it will automatically save the user key.

        It will also always return the server response which contains any errors provided.
        '''
        data = {'name': name, 'password': password}
        res = self.send_req_raw('/login', data=data)
        if res != 0 and res['error'] == None:
            self.data['key'] = res['key']
            self.save_data()
        return res

    def signup(self, name, password):
        '''
        Signs up to the server using the given username and password.
        If there are no errors, it will automatically save the user key.

        It will also always return the server response which contains any errors provided.
        '''
        data = {'name': name, 'password': password}
        res = self.send_req_raw('/signup', data=data)
        if res != 0 and res['error'] == None:
            self.data['key'] = res['key']
            self.save_data()
        return res

    def send_message(self, chat_id, message):
        '''Sends a message to the specified chat id.'''
        data = {
            'key': self.data['key'], 
            'action': 'send-message',
            'data': {'message': message}
        }
        res = self.send_req_raw('/chat/' + chat_id, data)
        return res
    
    def req_messages(self, chat_id, amount):
        '''
        Requests a list of the most recent messages.
        
        The amount of messages it requests is specified by the amount.
        (The maximum amount of messages to request is 100.)
        '''
        data = {
            'key': self.data['key'],
            'action': 'get-messages',
            'data': {'amount': amount}
        }
        res = self.send_req_raw('/chat/' + chat_id, data)
        return res

    def req_chats(self):
        '''
        
        '''
        data = {
            'key': self.data['key'],
            'action': 'get-chats'
        }
        res = self.send_req_raw('/chat' , data)
        if res['error'] == None:
            self.data['cache']['known-chats'] = res['chats']
            self.save_data()
        return res
        

if __name__ == '__main__':
    client = Client()
    client.login('Thbop', 'Beef64')
    chat_id = client.get_known_chats()[0]

    client.req_chats()


    # print(client.send_message(chat_id, 'Jag tycker om ost.'))

    # messages = client.req_messages(chat_id, 2)
    # for m in messages['data']:
    #     print(f"{ m['user'] } [{ m['timestamp'] }]: { m['content'] }")

