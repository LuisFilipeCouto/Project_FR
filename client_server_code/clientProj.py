import socket
import signal
import sys
import datetime
import struct
import psutil
import time

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

ip_addr = "127.0.0.1"
tcp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip_addr, tcp_port))

order=0

print('PC - ' + str(sock.getsockname()[0]) + ":" + str(sock.getsockname()[1]) + '\n')
print('Press Ctrl+C to exit...')

while True:
    try: 
        time.sleep(3)
        message=('PC: ' + str(sock.getsockname()[0]) + ':' + str(sock.getsockname()[1]) + '\n' + '[ CPU utilization: ' + str(psutil.cpu_percent()) + '%' + ' ]\n' + '[ Total RAM: ' + str(psutil.virtual_memory()[0]) + ' ]\n' + '[ Used RAM: ' + str(psutil.virtual_memory()[3]) + ' - ' + str(psutil.virtual_memory()[2]) + '% ]' + '\n').encode()
        version=1
        order+=1
        size=len(message)
        pkt=struct.pack('!BLL{}s'.format(size),version,size,order,message)
        sock.send(pkt)
    except (socket.timeout, socket.error):
        print('Server error. Done!')
        sys.exit(0)

