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
    EMPTY = 0.00
    GET = 0.01
    POST = 0.02
    SEARCH = 0.08

