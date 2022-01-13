import numpy as np
import json

from src.CoAP.constants import *

json_encoder=json.JSONEncoder()

class Message:
    """
        Implementeaza formatul de mesaj.
    """

    def __init__(self,m_type:int,token_len:int,m_class:int,m_code:int,m_id:int,payload:str,version=DEFAULT_VERSION,token=0x0):
        self.version=version
        self.m_type=m_type
        self.token_len=token_len
        self.m_class=m_class
        self.m_code=m_code
        self.m_id=m_id
        self.token=token #de tip bytes
        self.payload=payload


    @classmethod
    def decode(cls,data:bytes) -> 'Message':
        """
        :param data:  mesaj sub forma de octeti
        :return: mesaj decodat

        Decodarea este realizata conform modelului gasit la https://en.wikipedia.org/wiki/Constrained_Application_Protocol
        """

        version=(0xC0 & data[0])>>6
        m_type=(0x30 & data[0])>>4
        token_len=(0x0F & data[0])>>0
        m_class=((data[1]>>5)&0x07)
        m_code=((data[1]>>0)&0x1F)
        m_id=(data[2]<<8)|(data[3])


        # "Lengths 9-15 are reserved, MUST NOT be sent, and MUST be processed as a message format error."
        if(token_len>=9 and token_len<=15):
            print("Message format error")

        if(version != 1):
            print("Message ignored")

        #un octet este pastrat pt payload marker = 0xFF
        payload=data[5+token_len:].decode('utf-8')
        token=0
        if(token_len):
            token=data[4:(4+token_len)]

        return cls(m_type,token_len,m_class,m_code,m_id,payload,version,token)



    def to_bytes(self): #toBytes
        """
        :return: mesajul codificat sub forma de octeti
        """

        data=[]

        data.append((0x03 & self.version)<<6)
        data[0] |= ((self.m_type & 0x03)<<4)
        data[0] |= (self.token_len & 0x0f)

        data.append((self.m_class & 0x07)<<5)
        data[1] |= (self.m_code & 0x1f)

        data.append((self.m_id & 0xff00)  >> 8)
        data.append(self.m_id & 0xff)

        if(self.token_len > 0):
            for i in range (0,self.token_len):
                data.append(self.token[i])


        if(len(self.payload)>0):

            #PAYLOAD MARKER
            data.append(0xff)
            payload=self.payload.encode('utf-8')
            for i in range(0,len(payload)):
                data.append(payload[i])


        return bytes(data)




    def __str__(self):
        display = ""
        display += "version:{} \n ".format(self.version)
        display += "type:{} \n ".format(self.m_type)
        display += "token_len:{} \n ".format(self.token_len)
        display += "class:{} \n ".format(self.m_class)
        display += "code: {} \n".format(self.m_code)
        display += "message_id:{} \n".format(self.m_id)
        display += "token: {} \n".format(self.token)
        display += "payload: {} \n".format(self.payload)

        return display


    def get_code(self):
        """
            Functie utilizata pentru afisare in fisierul log.
        """
        m=''
        if self.m_class==CLASS_METHOD:
            if self.m_code==0:
                m='EMPTY'
            elif self.m_code==1:
                m='GET'
            elif self.m_code==2:
                m='POST'
            elif self.m_code==8:
                m='SEARCH'
        elif self.m_class==CLASS_SUCCESS:
            if self.m_code==1:
                m='CREATED'
            elif self.m_code==2:
                m='DELETED'
            elif self.m_code==3:
                m='VALID'
            elif self.m_code==4:
                m='CHANGED'
            elif self.m_code==5:
                m='CONTENT'
        elif self.m_class==CLASS_CLIENT_ERROR:
            if self.m_code==0:
                m='BAD_REQUEST'
            elif self.m_code==1:
                m='UNAUTHORIZED'
            elif self.m_code==2:
                m='BAD_OPTION'
            elif self.m_code==3:
                m='FORBIDDEN'
            elif self.m_code==4:
                m='NOT_FOUND'
            elif self.m_code==5:
                m='NOT_ALLOWED'
        elif self.m_class==CLASS_SERVER_ERROR:
            if self.m_code==0:
                m='INTERNAL_SERVER_ERROR'
            elif self.m_code==1:
                m='NOT_IMPLEMENTED'
            elif self.m_code==2:
                m='BAD_GATEWAY'
            elif self.m_code==3:
                m='UNAVAILABLE_SERVICE'
        return m



    def get_class(self):
        """
            Functie utilizata pentru afisare in fisierul log.
        """
        c=''
        if self.m_class==0:
            c='METHOD'
        elif self.m_class==2:
            c='SUCCES'
        elif self.m_class==4:
            c='CLIENT_ERROR'
        elif self.m_class==5:
            c='SERVER_ERROR'

        return c


    def get_type(self):
        """
            Functie utilizata pentru afisare in fisierul log.
        """
        t=''
        if self.m_type==0:
            t='CON'
        elif self.m_type==1:
            t='NON_CON'
        elif self.m_type==2:
            t='ACK'
        elif self.m_type==3:
            t='RESET'

        return t