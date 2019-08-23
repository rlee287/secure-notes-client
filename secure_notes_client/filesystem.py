import os
import os.path
import json

class DirectoryPush(object):

    def __init__(self,directory):
        self.olddir=os.getcwd()
        if not os.path.isdir(directory):
            raise ValueError("Specified directory is invalid!")
        self.chdir=directory

    def __entry__(self):
        os.chdir(self.chdir)
        return self.chdir

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.olddir)
        return False

def populate_userdir(config_obj, password):
    if not config_obj.username:
        raise ValueError("Username must be set before populating directory")
    userdir_existed=os.path.isdir(config_obj.userdir)

    if not userdir_existed:
        os.mkdir(config_obj.userdir)
        if not os.path.isfile(config_obj.user_salt_file):
            key_salt=os.urandom(16)
            with open(config_obj.user_salt_file,"wb") as fil:
                fil.write(key_salt)
    else:
        if not os.path.isfile(config_obj.user_salt_file):
            #throw huge warning
            return

#Note I/O which is basically format checking+encryption/decryption
def write_noteobj(config_obj,note_obj):
    id_name=note_obj["note"]["_id"]
    filepath=os.path.join(config_obj.userdir,"{}.json".format(id_name))
    with open(filepath,"w") as fil:
        json.dump(note_obj,fil)

def read_noteobj(config_obj,note_id):
    filepath=os.path.join(config_obj.userdir,"{}.json".format(note_id))
    with open(filepath,"r") as fil:
        note_info=json.load(fil)
    return note_info
