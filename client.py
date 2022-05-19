
import socket
import json
import os

import putHandler

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverAddress = ('localhost', 10000)

payload = {
    "command": "put",
    "fileName": "grandeFile.txt"
}

try:
    
    if(not os.path.exists(payload['fileName'])):
        print('File not exists')
        socketUDP.close()
    
    print('sending put command')
    socketUDP.sendto(json.dumps(payload).encode(), serverAddress)
    
    #wait for command ack
    
    socketUDP.settimeout(0.5)
    
    try:    
        ready, address = socketUDP.recvfrom(4096)
    except socket.timeout:
        print("Error during command transmission, closing socket")   
        socketUDP.close()
    
    socketUDP.settimeout(None)
    
    putHandler.rdtFileDataSender(payload['fileName'], socketUDP, serverAddress)

except Exception as info:
    print(info)
finally: 
    print('closing socket')
    socketUDP.close()