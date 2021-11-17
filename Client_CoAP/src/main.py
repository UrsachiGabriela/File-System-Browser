from src.Client.CoAPclient import CoAPclient
from src.GUI.Interface import Window
import json
if __name__=='__main__':
     app= Window()
     app.window.mainloop()

     #
     # client=CoAPclient(10001,10002,'127.0.0.1')
     #
     # client.endConnection()
     # client.startConnection()




