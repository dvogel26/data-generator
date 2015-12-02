
# data-generator.py
#
# Creates and sends data to data-server.py 
#
# Usage: python data-generator.py 
#    or
# . docker.env; docker run -d --name data-generator_$SERVER_UNIX_PORT --env-file=docker.env -p $SERVER_UNIX_PORT:$SERVER_PORT dvogel26/data-generator
#    or
# . docker.env; docker run -d --name data-generator_$SERVER_PORT --env-file=docker.env --net=host dvogel26/data-generator
#
# Build: docker build -t dvogel26/data-generator .

import os
import socket
import sys
import time

SERVER_PORT = int(os.getenv('SERVER_PORT'))
SERVER_HOST = os.getenv('SERVER_HOST')
PAUSE = os.getenv('PAUSE', 2)
VERBOSE = int(os.getenv('VERBOSE', 0))
PFX = 'data-generator.py:'

def check_env():
    fail = False
    if SERVER_PORT == None:
        sys.stderr.write('Usage: SERVER_PORT environment variable not set\n')
        fail = True
    if SERVER_HOST == None:
        sys.stderr.write('Usage: SERVER_HOST environment variable not set\n')
        fail = True
    if fail:
        sys.exit(1)

def main():
    print PFX, 'Starting'
    check_env()

    print PFX, 'trying to connect to data_server.py on', SERVER_HOST + ':' + str(SERVER_PORT)
    out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            out_socket.connect((SERVER_HOST, SERVER_PORT))
            break
        except:
            time.sleep(5)
    print PFX, 'connected'

    # send data to data_server.py
    i = 0
    while True:
        try:
            i += 1
            msg = 'datum ' + str(i)
            if VERBOSE > 1:
                print PFX, msg
            out_socket.send(msg)
            time.sleep(PAUSE)
        except:
            print 'Caught interrupt; quitting'
            out_socket.close()
            sys.exit(1)

main()


