import random
import socket
from math import log,ceil

from src.CoAP.constants import Type,Code,Class,Param
from src.CoAP.CoAPpackage import Message
from src.CoAP.commands import Command, detailsCommand


class CoAPclient():
    def __init__(self,myPort:int,serverPort:int,serverIp:str):
        self.myPort=myPort
        self.serverPort=serverPort
        self.serverIp=serverIp
        self.mySocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


        self.msg_id=-1




    def startConnection(self):
        self.mySocket.bind( ('0.0.0.0', int(self.myPort)))
        print('Connection started. :) ')

        self.mySocket.sendto(bytes("Salut",encoding="ascii"),(self.serverIp,int(self.serverPort)))
        data,address=self.mySocket.recvfrom(1024)
        print("S-a receptionat ", str(data), " de la ", address)


    def run(self):
        self.running=True
        # !!!!!!!!!!!!!!!!!!!!
        cmd=detailsCommand("path")







    # se creeaza o cerere in functie de comanda primita din interfata
    def createRequest(self,cmd,type:Type)->Message:
        msg_class=cmd.getClass()
        msg_code=cmd.getCode()
        msg_payload=cmd.payload()
        msg_type=type

        self.msg_id+=1

        token=self.generateToken()
        token_len=self.bytes_needed(token)

        msg=Message(msg_type,token_len,msg_class,msg_code,self.msg_id,msg_payload,token)

        return msg



    # se trimite pachet catre server ( sub forma de octeti )
    def send(self,msg:Message):
        self.mySocket.sendto(msg.encode(),(self.serverIp,int(self.serverPort)))

    # se primeste pachet de la server ( sub forma de octeti )
    def receive(self)->Message: #receive bytes from server and decode them
        fromServer,addr=self.mySocket.recvfrom(1024)
        return Message.decode(fromServer)


    def generateToken(self):
        return random.randint(0,0xffffffffffffffff)


    # token_len
    def bytes_needed(self,token):
       if token == 0:
           return 1
       return int(ceil(log(token, 256)))


    def endConnection(self):
        self.running=False
        self.mySocket.close()
        print('Connection stopped. :( ')


        # 64ko
