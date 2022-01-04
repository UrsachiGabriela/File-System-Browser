import numpy as np
import json

from src.CoAP.constants import *

json_encoder=json.JSONEncoder()

class Message:
    def __init__(self,m_type:int,token_len:int,m_class:int,m_code:int,m_id:int,payload:str,version=DEFAULT_VERSION,token=0):
        self.version=version
        self.m_type=m_type
        self.token_len=token_len
        self.m_class=m_class
        self.m_code=m_code
        self.m_id=m_id
        self.token=token #de tip bytes
        self.payload=payload

    @classmethod
    def decode(cls,data:bytes) -> 'Message': #extractFromBytes
        version=(0xC0 & data[0])>>6
        m_type=(0x30 & data[0])>>4
        token_len=(0x0F & data[0])>>0
        m_class=((data[1]>>5)&0x07)
        m_code=((data[1]>>0)&0x1F)
        m_id=(data[2]<<8)|(data[3])

        #length 9-15 are reserved
        if(token_len>=9 and token_len<=15):
            print("error")

        if(version != 1):
            print("error")

        #un octet este pastrat pt payload marker = 0xFF
        payload=data[5+token_len:].decode('utf-8')
        token=0
        if(token_len):
            token=data[4:(4+token_len)]

        return cls(m_type,token_len,m_class,m_code,m_id,payload,version,token)

        #struct module -- pack/unpack pack('i i 4s',3,4,'trgtr')

    def to_bytes(self): #toBytes
        data=[]

        data.append((0x03 & self.version)<<6)
        data[0] |= ((self.m_type & 0x03)<<4)
        data[0] |= (self.token_len & 0x0f)

        data.append((self.m_class & 0x07)<<5)
        data[1] |= (self.m_code & 0x1f)

        data.append((self.m_id & 0xff00)  >> 8)
        data.append(self.m_id & 0xff)

        if(self.token_len > 0):

            #aux=self.token.to_bytes(self.token_len,'big')
            #aux=bytearray(aux)

            for i in range (0,self.token_len):
                data.append(self.token[i])


        if(len(self.payload)>0):
            #PAYLOAD MARKER
            data.append(0xff)
            payload=self.payload.encode('utf-8')
            for i in range(0,len(payload)):
                data.append(payload[i])

        #a = np.array(data)
        #a.tobytes(order='F')




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



