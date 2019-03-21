import hashlib
import socket
import sys
import time
from udp_const import ACK_MSG, STOP_AND_WAIT_ENABLED, MSG_SHA_SIG, EOF_char

if len(sys.argv) != 4:
    print("usage: python3 %s <ip_addr> <port> <data_unit_size_in_bytes>" % sys.argv[0])
    sys.exit()

UDP_IP_ADDRESS = sys.argv[1]
UDP_PORT_NO = int(sys.argv[2])
DATA_UNIT_SIZE_IN_BYTES = int(sys.argv[3])
    
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

