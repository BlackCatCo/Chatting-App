import secrets

class User:
    def __init__(self, db):
        # Maybe add a friends system
        self.default_user = {
            'key':None,
            'name':None,
            'password':None,
            'permission-level':0
        }
        self.db = db

    def get(self, key):
        '''Get's a user's data using their key.'''
        output = None
        for user in self.db.data['users']:
            if user['key'] == key:
                output = user
        
        return output

    
    def get_name(self, name):
        '''Get's a user's data using their name.'''
        user = None
        for u in self.db.data['users']:
            if name.lower() == u['name'].lower():
                user = u
        return user
    
    def add(self, name, password):
        '''
        Checks for name duplicates, and if the
        coast is clear: add user and save to database.
        '''
        if self.get_name(name) == None:
            user = self.default_user.copy()

            user['key'] = secrets.token_hex()
            user['name'] = name
            user['password'] = password

            self.db.data['users'].append(user)
            self.db.save()
           
            return True
        else:
            return False
    
    def add_raw(self, user):
        self.db.data['users'].append(user)
        self.db.save()
    
    def edit(self, key, k, v):
        '''Edits a user via the specified key and key/value pair'''
        user_i = None
        for i, user in enumerate(self.db.data['users'], 0):
            if key == user['key']:
                user_i = i
        if user_i == None:
            return False
        else:
            self.db.data['users'][user_i][k] = v
            self.db.save()
            return True

    
    def migrate(self):
        '''
        Migrates the user database to the current user version.
        "self.default_user" defines what the current user stores and "self.migrate()"
        will update all users to be like "self.default_user."
        '''
        new_users = []
        for old_user in self.db.data['users']:
            new_user = self.default_user.copy()
            for k in old_user:
                if k in new_user:
                    new_user[k] = old_user[k]

            new_users.append(new_user)
        self.db.data['users'] = new_users

        self.ai.migrate()
        self.db.save()
    
    def remove(self, key):
        '''Removes a user from the database using the given key.'''
        user = self.get(key)
        if user != None:
            self.db.data['users'].remove(user)
            self.db.save()
            return True
        else:
            return False
    
    def check_login(self, name, password):
        '''
        Checks for a valid login using the given name and password.
        Returns the user if valid, otherwise returns False.
        '''
        user = self.get_name(name)
        if user != None and user['password'] == password:
            return self.get_name(name)
        else:
            return False