import hashlib
import socket
import sys
import time
from udp_const import UDP_IP_ADDRESS, UDP_PORT_NO, DATA_UNIT_SIZE_IN_BYTES, ACK_MSG, STOP_AND_WAIT_ENABLED, MSG_SHA_SIG, EOF_char

serverSock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
ackSock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fsm_state = 0
rcv_msg_SHA256 = hashlib.sha256()

while True:
    curr_msg_size = (fsm_state+1) * DATA_UNIT_SIZE_IN_BYTES

    data, addr = serverSock.recvfrom(curr_msg_size)
    rcv_msg_SHA256.update(data)
    print("msg: %s" % data)
    
    # TODO: check for EOF
    if data in EOF_char:
        # measure time taken
        print(time.time())
        # verify file integrity by SHA
        print(rcv_msg_SHA256.hexdigest() == MSG_SHA_SIG)
    
    # send ack
    ackSock.sendto(ACK_MSG, (UDP_IP_ADDRESS, UDP_PORT_NO+1))
    
    if STOP_AND_WAIT_ENABLED:
        fsm_state = (fsm_state + 1) % 4
    else:
        fsm_state = 0 # alwaus expect 1 Data Unit

