import hashlib
import socket
import sys
import time
from udp_const import UDP_PORT_NO, ACK_MSG, STOP_AND_WAIT_ENABLED, MSG_SHA_SIG, EOF_char

if len(sys.argv) != 4:
    print("usage: python3 %s <server_ip_addr> <client_ip_addr> <data_unit_size_in_bytes>" % sys.argv[0])
    sys.exit()

UDP_SERVER_IP_ADDRESS = sys.argv[1]
UDP_CLIENT_IP_ADDRESS = sys.argv[2]
DATA_UNIT_SIZE_IN_BYTES = int(sys.argv[3])
    
serverSock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_SERVER_IP_ADDRESS, UDP_PORT_NO))
ackSock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fsm_state = 0
recv_msg = ''

while True:
    for _ in range(fsm_state+1):
        data, addr = serverSock.recvfrom(DATA_UNIT_SIZE_IN_BYTES)
        #rcv_msg_SHA256.update(data)
        recv_msg += data
        print("msg: %s" % data) # maybe shouldn't print data, slow

        # DONE: check for EOF
        if EOF_char in data:
            # verify file integrity by SHA
            recv_msg_sha = hashlib.sha256(recv_msg).hexdigest()
            print(recv_msg_sha)
            print(MSG_SHA_SIG)
            if recv_msg_sha == MSG_SHA_SIG:
                ackSock.sendto(ACK_MSG, (UDP_CLIENT_IP_ADDRESS, UDP_PORT_NO))
            break

    ackSock.sendto(ACK_MSG, (UDP_CLIENT_IP_ADDRESS, UDP_PORT_NO))

    if STOP_AND_WAIT_ENABLED == False:
        fsm_state = (fsm_state + 1) % 4
    else:
        fsm_state = 0 # alwaus expect 1 Data Unit

