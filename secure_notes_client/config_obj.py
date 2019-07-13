import os.path
import base64

from argon2.low_level import Type, hash_secret_raw

class ConfigObj:
    def __init__(self):
        #Call @property things
        self.basedir=os.path.expanduser("~/.secure_notes")
        self.username=""
        self.token=""
        self.key=""
        self.url="http://127.0.0.1:5000"
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self,usern):
        #Simultaneously invalidate token and key which are per-username
        self.token=""
        self.key=""
        self._username=usern
    
    @property
    def userdir(self):
        username_64=base64.b64encode(self.username.encode("utf-8")).decode("ascii")
        return os.path.join(self.basedir,username_64)
    
    @property
    def user_salt_file(self):
        return os.path.join(self.userdir,"key_salt")
    
    def update_key(self,password):
        if not self.username:
            raise ValueError("Username must be set before key derivation")
        if not os.path.isfile(self.user_salt_file):
            raise ValueError("User directory must be populated before key derivation")
        with open(self.user_salt_file,"rb") as fil:
            key_salt=fil.read()
        key_val=hash_secret_raw(password.encode("utf-8"),key_salt,
                                10,409600,4,
                                16,
                                Type.ID)
        self.key=key_val

    #Make sure this is idempotent!
    def __del__(self):
        try:
            del self.token
        except AttributeError:
            pass
        try:
            del self.key
        except AttributeError:
            pass
