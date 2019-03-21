import hashlib

ACK_MSG = bytes.fromhex('dead')
EOF_char = b'\xFF'

#UDP_IP_ADDRESS = "127.0.0.1"
#UDP_PORT_NO = 6789
#DATA_UNIT_SIZE_IN_BYTES = 1
STOP_AND_WAIT_ENABLED = False

MSG = "Hello, Server".encode() + EOF_char
MSG_SHA_SIG = hashlib.sha256(MSG).hexdigest()

