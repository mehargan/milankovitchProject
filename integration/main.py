import socket 
import time
import serial
from inputDetection import InputDetection

# Setup UDP server
UDP_IP = "127.0.0.1"
UDP_PORT = 5065

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

inp = InputDetection()

# Send serial data
# arduino = serial.Serial('COM9', 115200, timeout=1)
# count = 0

# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data
# while True:
#     num = input("Enter a number: ") # Taking input from user
#     value = write_read(num)
#     print(value) # printing the value

while True:
    # Receive ecc and precession from stdin
    param = input('Enter precession, eccentricity as [ecc|prec]:')

    sock.sendto((param).encode(), (UDP_IP, UDP_PORT))
    
    # omega, ecc = inp.detection_loop(True)

    # if not omega is None: 
    #     print(f'Precession angle: {omega}')

    #     # Send to Unity over UDP
    #     sock.sendto(("GOT PREC").encode(), (UDP_IP, UDP_PORT))