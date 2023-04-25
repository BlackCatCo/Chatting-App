# Chatting-App
##################################
***This project is paused either temporarily or indefinitely.***
###################################

This Chatting App is a nice little open-source flask application with some gui applets.

[NOTE]: This project is currently in an earily stage. This means that it doesn't work properly or at all.

## Codebase structure:
Its structure is quite odd yet simple to understand.
### Server:
The flask server will handle user, message, and "database" management while also serving the client with raw json.
You can create your own script to talk to the server if you wish, but I (Thbop) have in fact already done that.

### "client.py"
"client.py" contains a single "Client" class that manages user data and POST/GET requests. It provides simple and advanced methods for contacting the server
such as (but not limited to) ping, login, and send_message. After logins/signups it will also automatically save the user's auth key within the "client-data.json"
file.

### GUI
This part is up to you! We are actually working on two different GUI applications that will use the "Client" class to correspond with the server, but if you 
do not like our designs, feel free to make your own!

## UI Structure
Currently, we have a very simple structure of only DM chats/group chats.
