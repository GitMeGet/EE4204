import hashlib

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
DATA_UNIT_SIZE_IN_BYTES = 1

ACK_MSG = bytes.fromhex('dead')
STOP_AND_WAIT_ENABLED = False

EOF_char = b'\xFF'
MSG = "Hello, Server".encode() + EOF_char
MSG_SHA_SIG = hashlib.sha256(MSG).hexdigest()

