import secrets
from time import strftime



class Chat:
    def __init__(self, db):
        self.db = db
    
    def get(self, chat_id):
        out = None
        for chat in self.db.data['chats']:
            if chat['id'] == chat_id:
                out = chat
        return out

    def get_title(self, title):
        out = None
        for chat in self.db.data['chats']:
            if chat['title'] == title:
                out = chat
        return out

    def get_index(self, chat_id):
        index = None
        for i, chat in enumerate(self.db.data['chats'], 0):
            if chat['id'] == chat_id:
                index = i
        return index

    def add(self): pass # User secrets.token_hex() for chat id

    def remove(self): pass

    def send(self, chat_id, name, content):
        chat_index = self.get_index(chat_id)
        if chat_index != None:
            message = {
                'user': name,
                'content': content,
                'timestamp': strftime('%m-%d-%y %H:%M')
            }
            self.db.data['chats'][chat_index]['messages'].append(message)
            self.db.save()
            return True
        else:
            return False
    
    def get_messages(self, chat_id, amount):
        if amount > 100: # Set a cap on the amount of messages reqested.
            amount = 100
        chat = self.get(chat_id)
        if chat == None:
            return None
        else:
            if len(chat['messages']) < amount:
                return chat['messages']
            else:
                return chat['messages'][ len(chat['messages']) - amount:]