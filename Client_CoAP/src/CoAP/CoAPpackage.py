
class Message:
    def __init__(self,m_type:int,token_len:int,m_class:int,m_code:int,m_id:int,payload:str,version=1,token=0):
        self.version=version
        self.m_type=m_type
        self.token_len=token_len
        self.m_class=m_class
        self.m_code=m_code
        self.m_id=m_id
        self.token=token
        self.payload=payload

    @classmethod
    def extractFromBytes(cls,data:bytes):
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
        if(token_len):
            token=data[4:4+token_len]

        return cls(m_type,token_len,m_class,m_code,m_id,payload,version,token)



    def toBytes(self):
        data=0x00
        data=data|self.version<<6
        #....


        return bytes(data)






