import time
import socket
import sys
import logging
logging.basicConfig(level=logging.INFO)

from udp_const import UDP_PORT_NO, ACK_MSG, STOP_AND_WAIT_ENABLED, MSG

if len(sys.argv) != 4:
    print("usage: python3 %s <server_ip_addr> <client_ip_addr> <data_unit_size_in_bytes>" % sys.argv[0])
    sys.exit()

UDP_SERVER_IP_ADDRESS = sys.argv[1]
UDP_CLIENT_IP_ADDRESS = sys.argv[2]
DATA_UNIT_SIZE_IN_BYTES = int(sys.argv[3])

# socket.AF_INET represent the address (and protocol) families
# socket.SOCK_DGRAM represent the socket types
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ackSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ackSock.bind((UDP_CLIENT_IP_ADDRESS, UDP_PORT_NO))

msg_idx = 0
fsm_state = 0

# record tx start time
start_time = time.time()

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
    
    if STOP_AND_WAIT_ENABLED == False:
        fsm_state = (fsm_state + 1) % 4
    else:
        fsm_state = 0 # alwaus expect 1 Data Unit

# record end time
end_time = time.time()
msg_tx_time = end_time - start_time
throughput = (len(MSG) * 8)/msg_tx_time

# log start, end, total time
with open("udp.log", 'a') as f:
    f.write("msg_len_in_bytes: %d \ndata_unit_size_in_bytes: %d \nstop_and_wait_enabled: %s \nstart_time: %f \nend_time: %f \ntotal_time_in_secs: %f \nthroughput_in_bits_per_sec: %f \n\n" % (len(MSG), DATA_UNIT_SIZE_IN_BYTES, str(STOP_AND_WAIT_ENABLED), start_time, end_time, msg_tx_time, throughput))

