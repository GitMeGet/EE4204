import time
import socket
import sys
import logging
logging.basicConfig(level=logging.INFO)

from udp_const import ACK_MSG, STOP_AND_WAIT_ENABLED, MSG

if len(sys.argv) != 5:
    print("usage: python3 %s <ip_addr> <port> <data_unit_size_in_bytes>" % sys.argv[0])
    sys.exit()

UDP_SERVER_IP_ADDRESS = sys.argv[1]
UDP_CLIENT_IP_ADDRESS = sys.argv[2]
UDP_PORT_NO = int(sys.argv[3])
DATA_UNIT_SIZE_IN_BYTES = int(sys.argv[4])

# socket.AF_INET represent the address (and protocol) families
# socket.SOCK_DGRAM represent the socket types
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ackSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ackSock.bind((UDP_CLIENT_IP_ADDRESS, UDP_PORT_NO))

msg_idx = 0
fsm_state = 0

print(time.time())

while msg_idx < len(MSG):
    curr_msg_size = (fsm_state+1) * DATA_UNIT_SIZE_IN_BYTES
    msg_end_idx = msg_idx + curr_msg_size
    
    if (msg_end_idx < len(MSG)):
        curr_msg = MSG[msg_idx: msg_end_idx]
    else:
        curr_msg = MSG[msg_idx:] # whatever's left of msg
    
    print("msg: %s" % curr_msg)
    clientSock.sendto(curr_msg, (UDP_SERVER_IP_ADDRESS, UDP_PORT_NO))
    
    # wait for ack
    data, addr = ackSock.recvfrom(len(ACK_MSG))
    if data == ACK_MSG:
        logging.debug('ack')
    else:
        logging.debug('ack failed')
    
    msg_idx += curr_msg_size
    
    if STOP_AND_WAIT_ENABLED:
        fsm_state = (fsm_state + 1) % 4
    else:
        fsm_state = 0 # alwaus expect 1 Data Unit