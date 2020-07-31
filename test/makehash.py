import hashlib
from datetime import datetime

#time stamp with set format for various funcions
def time():
        
    return str(datetime.now().strftime("%y%m%d%H%M"))

pwdhashobj = hashlib.sha256(("CAKETh!sIsW£akCAKE").encode('utf_8'))
hashvalue = time() + pwdhashobj.hexdigest()
outhashobj = hashlib.sha256(hashvalue.encode('utf_8'))

print(outhashobj.hexdigest())

