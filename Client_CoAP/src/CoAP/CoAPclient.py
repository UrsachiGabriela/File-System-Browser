import random
import secrets
import socket
from math import log,ceil
import queue
import json
import logging

json_encoder=json.JSONEncoder()
json_decoder=json.JSONDecoder()

from src.CoAP.CoAPpackage import Message
from src.CoAP.commands import *




class CoAPclient():
    def __init__(self,myPort:int,serverPort:int,serverIp:str,controller,message_queue:queue.Queue=None):
        self.myPort=myPort
        self.serverPort=serverPort
        self.serverIp=serverIp

        self.controller=controller

        self.mySocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.mySocket.bind( ('0.0.0.0', int(self.myPort)))
        self.mySocket.settimeout(self.random_timeout())

        self.running=False


        """
        https://www.loggly.com/ultimate-guide/python-logging-basics/
        """
        self.logger=logging.Logger(name='CoAP_client')
        handler=logging.FileHandler('client.log',mode='w')
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)


        self.message_queue=message_queue



    def run(self):
        try:
            self.logger.info(f'Started connection with ( {self.serverIp} , {self.serverPort} )')
            while(self.running):
                # se asteapta pana cand se da o comanda din interfata, pentru a o trimite la server
                cmd=self.controller.message_queue.get(block=True,timeout=None)
                request=self.create_request(cmd)


                self.logger.info(f'request   {request.get_type()} - {request.get_class()} - {request.get_code()}  :'+ request.payload)
                if(request.m_type==TYPE_NON_CON_MSG and cmd.response_needed()==False):
                    self.send(request) # se trimite cererea, fara a astepta raspuns sau ack de la server

                else : # mesaj confirmabil sau comanda care asteapta date de la server
                    response=self.match_response(request)
                    if response:
                        self.logger.info(f'response  {response.get_type()} - {response.get_class()} - {response.get_code()}  : ' + response.payload)
                        self.analyze_response(cmd,response)


        except (ConnectionResetError,WindowsError) as err :
            self.logger.error(err)
            self.mySocket.close()






    def analyze_response(self,cmd:Command,response:Message):

        if response.m_type==TYPE_RST:
            self.message_queue.put(cmd)
            return

        if response.m_class==CLASS_SUCCESS:
            data_from_server=json_decoder.decode(response.payload)
            if "status" in data_from_server:
                self.controller.show_message(data_from_server["status"])
            cmd.parse_response(data_from_server)
        elif response.m_class==CLASS_CLIENT_ERROR or response.m_class==CLASS_SERVER_ERROR:
            self.controller.show_message(response.payload)
        else:
            self.controller.show_message('Invalid response from server.')









    # se creeaza o cerere/un mesaj in functie de comanda primita din interfata
    def create_request(self, cmd)->Message:
        msg_class=cmd.get_class()
        msg_code=cmd.get_code()
        msg_payload=cmd.payload()

        msg_type=cmd.mType
        msg_id=self.generate_msg_ID()


        token_len=self.generate_token_len()

        #se genereaza un token aleatoriu de dimensiune token_len bytes
        token=self.generate_token(token_len)

        msg=Message(m_type=msg_type,token_len=token_len,m_class=msg_class,m_code=msg_code,m_id=msg_id,payload=msg_payload,version=1,token=token)

        return msg



    # se trimite pachet catre server ( sub forma de octeti )
    def send(self,msg:Message):
        self.mySocket.sendto(msg.to_bytes(), (self.serverIp, int(self.serverPort)))



    # se primeste pachet de la server ( sub forma de octeti )
    def receive(self)->Message:
        fromServer,addr=self.mySocket.recvfrom(1024)
        return Message.decode(fromServer)



    def match_response(self, request:Message)->Message:
        """
           Se trimite cererea : in cazul in care nu se primeste raspuns in intervalul de timp dat (mySocket.settimeout),
        se retrimite cererea, dar doar daca nu s-a atins un nr maxim (MAX_RETRANSMIT) de transmisii
        """

        transmitted=0
        while transmitted<MAX_RETRANSMIT :
            self.send(request)
            transmitted+=1
            try:
                response=self.receive()

                # request confirmabil
                if(request.m_type==TYPE_CON_MSG):

                    #astept pana cand primesc fie acknowledge, fie direct raspunsul pt cererea trimisa
                    while(not(response.m_id == request.m_id) and not(response.token == request.token)):
                        response=self.receive()


                    if response.m_id != request.m_id: # raspuns inainte de ack (response.token == request.token)
                        if response.m_type==TYPE_CON_MSG:
                            self.acknowledge_for_server(response)
                        return response
                    else: #response.m_id == request.m_id: ->  primesc intai ack

                        #s-a primit un raspuns cu acelasi msg_id ca al request-ului
                        #verific daca e ACK sau RESET


                        # daca e RESET il returnez, urmand ca interpretarea raspunsului sa fie facuta in fct separata
                        if response.m_type==TYPE_RST:
                            return response
                        elif response.m_type!=TYPE_ACK:
                            self.logger.info('error: ACK expected ')
                        else:
                            self.logger.info('Request acknowledged')



                        # verific daca am piggybacked response sau nu

                        # raspuns separat (ack de tip empty)
                        if(response.m_class==CLASS_METHOD and response.m_code==CODE_EMPTY and response.token_len==0 and  response.token is None ):
                            response=self.receive()

                            while(response.token != request.token):
                                response=self.receive()

                            # send acknowledge to server for con response
                            if response.m_type==TYPE_CON_MSG:
                                self.acknowledge_for_server(response)

                            return response
                        else:
                            #piggybacked
                            self.logger.info('Piggybacked response')
                            return response


                # request non-confirmabil
                elif (request.m_type==TYPE_NON_CON_MSG):
                    # daca cererea trimisa este non-confirmabila, se asteapta doar raspunsul (fara ack) cu acelasi token
                    while(response.token != request.token):
                        response=self.receive()

                    return response

            except (socket.timeout,ConnectionResetError,WindowsError) as err:
                self.logger.info(err)








    def generate_token_len(self):
        return random.randint(1,8)

    #generare token aleatoriu
    def generate_token(self, token_len):
        return secrets.token_bytes(token_len)




    def generate_msg_ID(self):
        return random.randint(0,0xffff)

    # token_len
    def bytes_needed(self,token):
       if token == 0:
           return 1
       return int(ceil(log(token, 256)))


    def end_connection(self):
        self.logger.info('Connection stopped.')




    def random_timeout(self):
        return random.uniform(ACK_TIMEOUT,ACK_TIMEOUT * ACK_RANDOM_FACTOR)

    def acknowledge_for_server(self,response:Message):
        ack=Message(m_type=TYPE_ACK,token_len=0,m_class=CLASS_METHOD,m_code=CODE_EMPTY,m_id=response.m_id,payload='',token=0x0)
        self.send(ack)


    def log_error(err):
        logging.error(f"Client error: {err}")