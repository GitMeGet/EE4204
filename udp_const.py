import hashlib
import random
random.seed(a=1)
import string

UDP_PORT_NO = 5350 # must use  this port for udp
#ACK_MSG = bytes.fromhex('dead') # py3.7
ACK_MSG = 'dead'.decode('hex') # py2.7
EOF_char = b'\xFF'

#UDP_IP_ADDRESS = "127.0.0.1"
#UDP_PORT_NO = 6789
#DATA_UNIT_SIZE_IN_BYTES = 1
STOP_AND_WAIT_ENABLED = False

MSG_LEN = 60000
#MSG = "Hello, Server".encode() + EOF_char
#MSG = (''.join('a' for _ in range(MSG_LEN))).encode() + EOF_char
MSG = (''.join(random.choice(string.ascii_letters) for _ in range(MSG_LEN))).encode() + EOF_char
MSG_SHA_SIG = hashlib.sha256(MSG).hexdigest()
