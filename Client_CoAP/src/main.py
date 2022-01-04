import json
import queue

from src.CoAP.CoAPclient import CoAPclient, json_encoder
from src.FileSystem.FS import File

if __name__=='__main__':


     client=CoAPclient(10001,10002,'127.0.0.1',queue.Queue())
     client.start_connection()


     #
     # p={
     #      "cmd":"move",
     #      "sourcePath":"self.sourcePath",
     #      "destinationPath":"self.destinationPath"
     # }
     # print(p["cmd"])
     #

     # for i in range(0,len(payload)):
     #      data.append(payload[i])
     #client.endConnection()



     # utilizare coada




     # interfata





     # port mapping/ forwarding


     #print(json_decoder.decode(Message.decode(msg.to_bytes()).payload)['cmd'])