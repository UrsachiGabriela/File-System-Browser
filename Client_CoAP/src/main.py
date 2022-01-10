import json
import queue

from src.CoAP.CoAPclient import CoAPclient, json_encoder
from src.GUI.application import Application

if __name__=='__main__':


     app=Application()
     #app.connect_to_server(10002,'127.0.0.1')
     app.mainloop()



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