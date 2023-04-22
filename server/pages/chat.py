from flask import request
import json

class Chat:
    def chat(self):
        @self.app.route('/chat', methods=['POST'])
        def chat():
            response = {'type': None, 'error':None}
            req = request.json
            enough_data = True

            try:
                key = req['key']
                action = req['action']
            except KeyError:
                response['error'] = 'Not enough data provided! Please send key and action.'
                enough_data = False
            
            if enough_data:
                user = self.handler.user.get(key)
                if user == None:
                    response['error'] = 'The user key provided is invalid and doesn not correspond to any user! Please provide another key.'
                else:
                    if action == 'get-chats':
                        response['chats'] = self.handler.chat.get_user_chats(user['name'])

            return json.dumps(response)
        

        @self.app.route('/chat/<chat_id>', methods=['POST'])
        def chat_id(chat_id):
            response = {'type': None, 'error':None}
            req = request.json
            enough_data = True

            chat = self.handler.chat.get(chat_id)
            if chat == None:
                response['error'] = 'Chat not found! There is no chat with the corresponding id. Please try another chat id.'
            else: # Chat is valid
                try:
                    key = req['key']
                    action = req['action']
                    data = req['data']
                except KeyError:
                    response['error'] = 'Not enough data provided! Please send key, action, and data.'
                    enough_data = False
                
                if enough_data: # If we have enough data to send a message...
                    user = self.handler.user.get(key)
                    if user == None:
                        response['error'] = 'The user key provided is invalid and doesn not correspond to any user! Please provide another key.'
                    else: # If the user is a valid user
                        if user['name'] not in chat['members']:
                            response['error'] = f'Chat "{ chat["id"] }" does not contain the member "{ user["name"] }."'
                        else: # If the user is in the chat
                            if action == 'send-message':
                                response['type'] = 'send-message'
                                try:
                                    message = data['message']
                                except KeyError:
                                    response['error'] = 'No message provided! Please provide a message in the data key.'
                                    enough_data = False

                                if enough_data: # If the message was provided
                                    self.handler.chat.send(chat_id, user['name'], message)

                            elif action == 'get-messages':
                                response['type'] = 'get-messages'
                                try:
                                    amount = data['amount']
                                except KeyError:
                                    response['error'] = 'No amount provided! Please provide a amount in the data key.'
                                    enough_data = False

                                if enough_data: # If the amount was provided
                                    response['data'] = self.handler.chat.get_messages(chat_id, amount)

            return json.dumps(response)

