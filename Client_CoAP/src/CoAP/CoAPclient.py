import random
import secrets
import socket
from math import log,ceil
import queue
import json

json_encoder=json.JSONEncoder()

from src.CoAP.CoAPpackage import Message
from src.CoAP.commands import *

# coada folosita pt a stoca cererile date din interfata pt a le trimite la server
q=queue.Queue(25)

class CoAPclient():
    def __init__(self,serverPort:int,serverIp:str):
        self.serverPort=serverPort
        self.serverIp=serverIp
        self.mySocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.mySocket.settimeout(self.randomTimeout())

        self.running=False




    def startConnection(self):
        #self.mySocket.bind( ('0.0.0.0', int(self.myPort)))
        print('Connection started. :) ')

        #self.mySocket.sendto(bytes("Salut",encoding="ascii"),(self.serverIp,int(self.serverPort)))
        #data,address=self.mySocket.recvfrom(1024)
        #print("S-a receptionat ", str(data), " de la ", address)


    def run(self):
        self.running=True

        while(self.running):
            # se asteapta pana cand se da o comanda din interfata, pentru a o trimite la server
            #cmd=q.get(block=True)

            cmd=openCommand('main.py')#provizoriu

            request=self.createRequest(cmd)
            print("Se trimite cererea la server: \n",request,"\n\n\n")

            if(request.m_type==TYPE_NON_CON_MSG and cmd.responseNeeded()==False):
                self.send(request) # se trimite cererea, fara a astepta raspuns sau ack de la server
            else : # mesaj confirmabil sau comanda care asteapta date de la server
                response=self.matchResponse(request)

                print("Raspuns de la server: \n", response)
                # se parseaza raspunsul



            self.running=False









    # se creeaza o cerere/un mesaj in functie de comanda primita din interfata
    def createRequest(self,cmd)->Message:
        msg_class=cmd.getClass()
        msg_code=cmd.getCode()
        msg_payload=cmd.payload()

        msg_type=cmd.mType
        msg_id=self.generateMsgID()
        #self.msg_id+=1

        token_len=self.generateTokenLen()
        #se genereaza un token aleatoriu de dimensiune token_len bytes
        token=self.generateToken(token_len)

        msg=Message(m_type=msg_type,token_len=token_len,m_class=msg_class,m_code=msg_code,m_id=msg_id,payload=msg_payload,version=1,token=token)

        return msg



    # se trimite pachet catre server ( sub forma de octeti )
    def send(self,msg:Message):
        self.mySocket.sendto(msg.toBytes(),(self.serverIp,int(self.serverPort)))

    # se primeste pachet de la server ( sub forma de octeti )
    def receive(self)->Message:
        fromServer,addr=self.mySocket.recvfrom(1024)
        return Message.decode(fromServer)



    def matchResponse(self,request:Message)->Message:
        # se trimite cererea : in cazul in care nu se primeste raspuns in intervalul de timp dat (mySocket.settimeout),
        # se retrimite cererea, dar doar daca nu s-a atins un nr maxim (MAX_RETRANSMIT) de transmisii
        transmitted=0
        while transmitted<MAX_RETRANSMIT :
            self.send(request)
            transmitted+=1
            try:
                response=self.receive()


            # request confirmabil
                if(request.m_type==TYPE_CON_MSG):
                    #se asteapta pana cand se primeste un mesaj de tip ack cu acelasi id

                    #while(not(response.m_type == TYPE_ACK and response.m_id == request.m_id)):
                    #    response=self.receive()  # se asteapta pana se primeste un ack de la server pt cererea trimisa


                    # ?????????---------------------------------------------------------------------------------------------

                    while(not(response.m_id == request.m_id)):
                        response=self.receive()  # se asteapta pana se primeste un ack de la server pt cererea trimisa

                    #s-a primit un raspuns cu acelasi msg_id ca al request-ului
                    #verific daca e ACK sau RESET

                    # daca e RESET il returnez, urmand ca interpretarea raspunsului sa fie facuta in fct separata
                    if response.m_type==TYPE_RST:
                        return response
                    elif response.m_type!=TYPE_ACK:
                        print("Error")
                        # exceptie???---------------------------------------------------------------------------------------------

                    # daca nu e RESET sau eroare => ACK
                    print("Request acknowledged")

                    # verific daca am piggybacked response sau nu

                    # raspuns separat
                    if(response.m_class==CLASS_METHOD and response.m_code==CODE_EMPTY and response.token_len==0 and  response.token is None ):
                        response=self.receive()

                        while(response.token != request.token):
                            response=self.receive()


                    return response
                    # daca raspunsul primit separat de ack este de tip con, ar trebui trimis un ack catre server !!

                # request non-confirmabil
                elif (request.m_type==TYPE_NON_CON_MSG):
                    # daca cererea trimisa este non-confirmabila, se asteapta doar raspunsul (fara ack) cu acelasi token
                    while(response.token != request.token):
                        response=self.receive()

                    return response

            except socket.timeout as e:
                print(e)




    def generateTokenLen(self):
        return random.randint(1,8)

    #generare token aleatoriu
    def generateToken(self,token_len):
        return secrets.token_bytes(token_len)




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

    def randomTimeout(self):
        return random.uniform(ACK_TIMEOUT,ACK_TIMEOUT * ACK_RANDOM_FACTOR)