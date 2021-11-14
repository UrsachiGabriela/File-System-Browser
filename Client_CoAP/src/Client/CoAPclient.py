import socket

class CoAPclient():
    def __init__(self,myPort:int,serverPort:int,serverIp:str):
        self.myPort=myPort
        self.serverPort=serverPort
        self.serverIp=serverIp
        self.mySocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def startConnection(self):
        self.mySocket.bind((serverIp, int(myPort))
        print('Connection started. :) ')

    def endConnection(self):
        self.mySocket.close()
        print('Connection stopped. :( ')