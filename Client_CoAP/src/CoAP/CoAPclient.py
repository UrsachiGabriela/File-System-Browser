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
    """
         Implementeaza clientul din aplicatia client-server.
         Acesta va rula intr-un thread separat de thread-ul principal.
    """

    def __init__(self,myPort:int,serverPort:int,serverIp:str,controller,message_queue:queue.Queue=None):
        """
            :param myPort: portul pe care se primesc pachete de la server
            :param serverPort: portul utilizat de server pentru primirea/transmiterea pachetelor
            :param serverIp: IP-ul server-ului
            :param controller: aplicatia care face legatura intre schimbul de pachete si interfata
            :param message_queue: coada de mesaje utilizata pentru comunicatia intre cele 2 thread-uri
        """
        self.myPort=myPort
        self.serverPort=serverPort
        self.serverIp=serverIp
        self.controller=controller

        # creare socket UDP
        self.mySocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.mySocket.bind( ('0.0.0.0', int(self.myPort)))

        # timeout aleatoriu stabilit pentru operatiile de la nivelul socket-ului
        self.mySocket.settimeout(self.random_timeout())

        self.running=False


        """
        https://www.loggly.com/ultimate-guide/python-logging-basics/
        """
        # creare fisier de logging
        self.logger=logging.Logger(name='CoAP_client')
        handler=logging.FileHandler('client.log',mode='w')
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)


        self.message_queue=message_queue



    def run(self):
        """
              Dupa ce se realizeaza conexiunea cu server-ul , clientul va prelua din coada de mesaje
            cereri confirmabile/non-confirmabile, pe care le trimite la server. In cazul cererilor care
            necesita un raspuns , se va procesa raspunsul primit , in functie de tipul comenzii generate
            din interfata.
        """
        try:
            self.logger.info(f'Started connection with ( {self.serverIp} , {self.serverPort} )')
            while(self.running):

                cmd=self.controller.message_queue.get(block=True,timeout=None)
                request=self.create_request(cmd)


                self.logger.info(f'request   {request.get_type()} - {request.get_class()} - {request.get_code()}  :'+ request.payload)

                if(request.m_type==TYPE_NON_CON_MSG and cmd.response_needed()==False):
                    # se trimite cererea, fara a astepta raspuns sau ack de la server
                    self.send(request)

                else :
                    # mesaj confirmabil sau comanda care asteapta date de la server
                    response=self.match_response(request)
                    if response:
                        self.logger.info(f'response  {response.get_type()} - {response.get_class()} - {response.get_code()}  : ' + response.payload +'\n')
                        self.analyze_response(cmd,response)


        except (ConnectionResetError,WindowsError) as err :
            self.logger.error(err)
            self.controller.destroy()







    def analyze_response(self,cmd:Command,response:Message):
        """
             Se proceseaza raspunsul primit de la server.

            :param cmd: comanda generata din interfata
            :param response: raspunsul la cererea ce contine comanda data
            :return:
        """

        # daca se primeste de la server un mesaj de tip RESET, se va retrimite cererea
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








    def create_request(self, cmd)->Message:
        """
            :param cmd:  comanda generata din interfata
            :return: pachetul construit pe baza comenzii date
        """

        msg_class=cmd.get_class()
        msg_code=cmd.get_code()
        msg_payload=cmd.payload()
        msg_type=cmd.mType
        msg_id=self.generate_msg_ID()
        token_len=self.generate_token_len()

        # se genereaza un token aleatoriu de dimensiune token_len bytes
        token=self.generate_token(token_len)

        msg=Message(m_type=msg_type,token_len=token_len,m_class=msg_class,m_code=msg_code,m_id=msg_id,payload=msg_payload,version=1,token=token)

        return msg



    def send(self,msg:Message):
        """
            :param msg: pachetul trimis la server
            :return:
        """
        self.mySocket.sendto(msg.to_bytes(), (self.serverIp, int(self.serverPort)))


    def receive(self)->Message:
        """
            :return: raspunsul de la server, in varianta decodata
        """
        fromServer,addr=self.mySocket.recvfrom(1024)
        return Message.decode(fromServer)



    def match_response(self, request:Message)->Message:
        """
           Se trimite cererea : in cazul in care nu se primeste raspuns in intervalul de
           timp dat (mySocket.settimeout),se retrimite cererea, dar doar daca nu s-a atins
           un nr maxim (MAX_RETRANSMIT) de transmisii.

           Pentru o cerere confirmabila, se asteapta fie un raspuns de tip ACKNOWLEDGE, fie
           un mesaj ce contine raspunsul asteptat (nemaifiind nevoie de alta confirmare)

           :param request: cererea trimisa server-ului
           :return: raspunsul ce corespunde cererii trimise
        """

        transmitted=0
        while transmitted<MAX_RETRANSMIT :
            self.send(request)
            transmitted+=1
            try:
                response=self.receive()

                # request confirmabil
                if(request.m_type==TYPE_CON_MSG):

                    # se asteapta pana cand se primeste fie acknowledge, fie direct raspunsul pt cererea trimisa
                    while(not(response.m_id == request.m_id) and not(response.token == request.token)):
                        response=self.receive()

                    # raspuns inainte de ack (response.token == request.token)
                    if response.m_id != request.m_id:
                        if response.m_type==TYPE_CON_MSG:
                            self.acknowledge_for_server(response)
                        return response

                    # nu se primeste direct raspunsul (response.m_id == request.m_id)
                    else:

                        if response.m_type==TYPE_RST:
                            return response
                        elif response.m_type!=TYPE_ACK:
                            self.logger.info('error: ACK expected ')
                        else:
                            self.logger.info('Request acknowledged')



                        # se verifica daca raspunsul primit este sau nu se tip piggybacked


                        # raspuns separat (ack de tip empty)
                        if(response.m_class==CLASS_METHOD and response.m_code==CODE_EMPTY and response.token_len==0 and  response.token is None ):
                            response=self.receive()

                            while(response.token != request.token):
                                response=self.receive()

                            # se trimite ack catre server pentru mesajele de tip CON primite
                            if response.m_type==TYPE_CON_MSG:
                                self.acknowledge_for_server(response)

                            return response

                        # raspuns de tip piggybacked
                        else:

                            self.logger.info('Piggybacked response')
                            return response


                # request non-confirmabil
                elif (request.m_type==TYPE_NON_CON_MSG):

                    # daca cererea trimisa este non-confirmabila, se asteapta doar raspunsul (fara ack) cu acelasi token
                    while(response.token != request.token):
                        response=self.receive()

                    return response

            except (socket.timeout) as err:
                self.logger.info(err)
            except (ConnectionResetError,WindowsError) as err2:
                self.logger.info(err2)
                self.controller.destroy()







    def generate_token_len(self):
        """
        :return: un intreg aleatoriu ce corespunde dimensiunii token-ului (in octeti)
        """
        return random.randint(1,8)


    def generate_token(self, token_len):
        """
        :param token_len: dimensiunea in octeti a token-ului
        :return: token-ul generat aleatoriu
        """
        return secrets.token_bytes(token_len)




    def generate_msg_ID(self):
        """
        :return: message ID generat aleatoriu
        """
        return random.randint(0,0xffff)



    def end_connection(self):
        """
          Se inchide conexiunea stabilita cu server-ul.
        """
        self.mySocket.close()
        self.logger.info('Connection stopped.')




    def random_timeout(self):
        """
        :return: timeout aleatoriu pentru primirea unui raspuns de la server la nivel de socket
        """
        return random.uniform(ACK_TIMEOUT,ACK_TIMEOUT * ACK_RANDOM_FACTOR)

    def acknowledge_for_server(self,response:Message):
        """
        :param response: mesaj confirmabil primit de la server
        """

        ack=Message(m_type=TYPE_ACK,token_len=0,m_class=CLASS_METHOD,m_code=CODE_EMPTY,m_id=response.m_id,payload='',token=0x0)
        self.send(ack)

