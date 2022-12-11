import socket 
import time
import serial
import math
import json 
from inputDetection import InputDetection, MAX_ECC
from milankovitch import MilankovitchTable

# Game states
GAME_INPUT = 0
GAME_START_ICEAGE = 1
GAME_START_NOICE  = 2
GAME_START_GLOW = 3

CURR_STATE = GAME_INPUT

# Simulation time for Snowglobe
SIM_TIME = 60

# Setup UDP server
UDP_IP = "127.0.0.1"
UDP_PORT = 5065

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

inp = InputDetection(1)

# Serial interface
arduino = serial.Serial('COM10', 115200, timeout=0.1)
# count = 0

def send_snowglobe(x):
    arduino.write(bytes(x, 'utf-8'))
    # time.sleep(0.05)
    # data = arduino.readline()
    # return data

def snowglobe_handshake():
    arduino.write(bytes('START', 'utf-8'))
    time.sleep(0.05)
    ack = str(arduino.readline())
    if ack == 'ACK': return True
    else: return False

# Wait for starting handshake with arduino
# while (not snowglobe_handshake()): pass

# Milankovitch Calculations
mtable = MilankovitchTable()
mtable.readMatrix()
mtable.readVostok()

def check_iceage(omega, ecc):
    if (math.isclose(ecc, MAX_ECC)):
        if (math.isclose(omega, 180.0, abs_tol=30.0)):
            return True

    return False

def get_json(params):
    json_str = '{ "state": ' + params[state] + ', ' + \
        '"year": ' + params[year] + ', ' + \
            '"eccen": ' + params[eccen] + ', ' + \
                '"omega": ' + params[omega] + ', ' + \
                    '"obliq": ' + params[obliq] + ', ' + \
                        '"insol": ' + params[insol] + ' }'
    return json_str

def adjust_omega(omega):
    tmp =  (omega + 290.0) if (omega - 70.0) < 0.0 else (omega - 70.0) 
    return tmp

while True:
    # Receive ecc and precession from stdin
    # omega = float(input('Enter precession: '))
    # ecc = float(input('Enter eccentricity: '))

    time.sleep(0.5)
    
    omega, ecc = inp.detect_parameters(True)

    # Skip if not found
    if (omega is None or ecc is None):
        continue

    # Convert omega to range [0, 360] from [-180, 180]
    omega = (360 + omega) % 360
    print(f'[INFO #55] Omega: {omega}, Eccentricity: {ecc}')


    # Get Milankovitch information
    params = mtable.lookUp(adjust_omega(omega), ecc)
    params['state'] = CURR_STATE

    # Check if GO Button pressed 
    if inp.check_start():
        # Check if Ice-Age condition met 
        ice_age = check_iceage(omega, ecc)

        if ice_age: 
            CURR_STATE = GAME_START_ICEAGE
            params['state'] = CURR_STATE

            # Convert dictionary to JSON and send to Unity
            json_str = json.dumps(params)
            sock.sendto((json_str).encode(), (UDP_IP, UDP_PORT))

            # Send signal to Snowglobe
            send_snowglobe('START')

            # Wait for 1 min
            time.sleep(SIM_TIME)

            # Send Game over signal 
            CURR_STATE = GAME_INPUT
            params['state'] = CURR_STATE
            json_str = json.dumps(params)
            sock.sendto((json_str).encode(), (UDP_IP, UDP_PORT))

        else:
            CURR_STATE = GAME_START_GLOW
            params['state'] = CURR_STATE

            # Convert to JSON and send to Unity
            json_str = json.dumps(params)
            sock.sendto((json_str).encode(), (UDP_IP, UDP_PORT))

            time.sleep(1)

            CURR_STATE = GAME_START_NOICE
            params['state'] = CURR_STATE

            # Convert to JSON and send to Unity
            json_str = json.dumps(params)
            sock.sendto((json_str).encode(), (UDP_IP, UDP_PORT))

    else: # GAME_INPUT state
        # Convert to dictionary and send to Unity
        json_str = json.dumps(params)
        sock.sendto((json_str).encode(), (UDP_IP, UDP_PORT))

    print(f'[INFO #96] {params}')
     