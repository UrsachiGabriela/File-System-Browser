import random
import socket
from math import log,ceil
import queue

from src.CoAP.constants import Param, TYPE_NON_CON_MSG, TYPE_CON_MSG, TYPE_ACK, CLASS_METHOD, CODE_EMPTY
from src.CoAP.CoAPpackage import Message
from src.CoAP.commands import *


class CoAPclient():
    def __init__(self,myPort:int,serverPort:int,serverIp:str):
        self.myPort=myPort
        self.serverPort=serverPort
        self.serverIp=serverIp
        self.mySocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


        self.msg_id=0
        self.running=False




    def startConnection(self):
        self.mySocket.bind( ('0.0.0.0', int(self.myPort)))
        print('Connection started. :) ')

        #self.mySocket.sendto(bytes("Salut",encoding="ascii"),(self.serverIp,int(self.serverPort)))
        #data,address=self.mySocket.recvfrom(1024)
        #print("S-a receptionat ", str(data), " de la ", address)


    def run(self):
        self.running=True

        q=queue.Queue(25)
        q.put(openCommand("openedPath"))
        # q.put(detailsCommand("openedPath"))
        # q.put(createCommand("openedPath","file"))
        # q.put(deleteCommand("openedPath"))

        # !!!!!!!!!!!!!!!!!!!!  provizoriu
        #while(self.running):
        while(not q.empty()):
            cmd=q.get()


            request=self.createRequest(cmd,TYPE_CON_MSG) #provizoriu
                                                         # se verifica tipul selectat din GUI,

            print("Se trimite cererea la server: \n",request,"\n\n\n")

            if(request.m_type==TYPE_NON_CON_MSG and cmd.responseNeeded()==False):
                self.send(request) # se trimite cererea, fara a astepta raspuns sau ack de la server
            else : # mesaj confirmabil sau comanda care asteapta date de la server
                self.send(request)
                response=self.matchResponse(request)

                print("Raspuns de la server: \n", response)
                # se parseaza raspunsul



            self.running=False









    # se creeaza o cerere/un mesaj in functie de comanda primita din interfata
    def createRequest(self,cmd,type)->Message:
        msg_class=cmd.getClass()
        msg_code=cmd.getCode()
        msg_payload=cmd.payload()
        msg_type=type
        msg_id=self.generateMsgID()
        #self.msg_id+=1

        token=self.generateToken()
        token_len=self.bytes_needed(token)

        msg=Message(m_type=msg_type,token_len=token_len,m_class=msg_class,m_code=msg_code,m_id=msg_id,payload=msg_payload,version=1,token=token)

        return msg



    # se trimite pachet catre server ( sub forma de octeti )
    def send(self,msg:Message):
        self.mySocket.sendto(msg.toBytes(),(self.serverIp,int(self.serverPort)))

    # se primeste pachet de la server ( sub forma de octeti )
    def receive(self)->Message: #receive bytes from server and decode them
        fromServer,addr=self.mySocket.recvfrom(1024)
        return Message.decode(fromServer)



    def matchResponse(self,request:Message)->Message:
        response=self.receive()

        # request confirmabil
        if(request.m_type==TYPE_CON_MSG):
            while(not(response.m_type == TYPE_ACK and response.m_id == request.m_id)):
                response=self.receive()  # se asteapta pana se primeste un ack de la server pt cererea trimisa


            print("Request acknowledged")

            # verific daca am piggybacked response sau nu

            # raspuns separat
            if(response.m_class==CLASS_METHOD and response.m_code==CODE_EMPTY and response.token_len==0 and  response.token is None ):
                response=self.receive()

                while(response.token != request.token):
                    response=self.receive()

        # request non-confirmabil
        elif (request.m_type==TYPE_NON_CON_MSG):
            response=self.receive()

            while(response.token != request.token):
                response=self.receive()

        return response


    #generare token aleatoriu
    def generateToken(self):
        return random.randint(0,0xff_ff_ff_ff_ff_ff_ff_ff)


    def generateMsgID(self):
        return random.randint(0,0xffff)

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
