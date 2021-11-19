from src.Client.CoAPclient import CoAPclient

import json
if __name__=='__main__':


     client=CoAPclient(10001,10002,'127.0.0.1')
     client.startConnection()
     #client.endConnection()





