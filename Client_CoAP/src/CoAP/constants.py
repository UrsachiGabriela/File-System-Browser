from enum import Enum

DEFAULT_VERSION = 1
ACK_TIMEOUT = 2
ACK_RANDOM_FACTOR  = 1.5
MAX_RETRANSMIT = 4

class Type(Enum):
    CON_MSG = 0
    NON_MSG = 1
    ACK = 2
    RST = 3

class Method(Enum):
    EMPTY = 0
    GET = 1
    POST = 2
    SEARCH = 8

