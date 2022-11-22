import socket 
import time
from inputDetection import InputDetection

# Setup UDP server
UDP_IP = "127.0.0.1"
UDP_PORT = 5065

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

inp = InputDetection()

while True:
    omega, ecc = inp.detection_loop(True)

    if not omega is None: 
        print(f'Precession angle: {omega}')

        # Send to Unity over UDP
        sock.sendto(("GOT PREC").encode(), (UDP_IP, UDP_PORT))