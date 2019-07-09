import os.path
import base64

class ConfigObj:
    def __init__(self):
        #Call @property things
        self.basedir=os.path.expanduser("~/.secure_notes")
        self.username=""
        self.token=""
        self.url="http://127.0.0.1:5000"
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self,usern):
        username_64=base64.b64encode(usern.encode("utf-8")).decode("ascii")
        self._username=usern
        self.userdir=os.path.join(self.basedir,username_64)
    
    #Make sure this is idempotent!
    def __del__(self):
        try:
            del self.token
        except AttributeError:
            pass
