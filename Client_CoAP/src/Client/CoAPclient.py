import socket

class CoAPclient():
    def __init__(self,myPort:int,serverPort:int,serverIp:str):
        self.myPort=myPort
        self.serverPort=serverPort
        self.serverIp=serverIp
        self.mySocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def startConnection(self):
        self.mySocket.bind( ('0.0.0.0', int(self.myPort)))
        print('Connection started. :) ')

        self.mySocket.sendto(bytes("Salut",encoding="ascii"),(self.serverIp,int(self.serverPort)))
        data,address=self.mySocket.recvfrom(1024)
        print("S-a receptionat ", str(data), " de la ", address)

    def endConnection(self):
        self.mySocket.close()
        print('Connection stopped. :( ')


        # 64ko
