
import socket
import os
import json

import rdt_handler

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 10000))

putHandler = rdt_handler.RdtFileTransferHandler();

while(True):
    
    #get command from client
    rawCommandPacket, address = s.recvfrom(4096)
    print('received message from %s %s' % (rawCommandPacket, address))
    
    commandPacket = json.loads(rawCommandPacket)
    
    command = commandPacket['command']
    
    #command switch for list, get, put
    
    if command == 'list':
        #send to client files list as json response
        files = json.dumps(os.listdir('./upload'))
        s.sendto(files.encode(), address)
    elif command == 'get':
        pass
    elif command == 'put':
        #send to client ready message to receive filename to upload
        print('Read Put')
        
        fileName = commandPacket['fileName']
        
        #send to client filename ack to receive file data
        s.sendto('FILENAME ACK'.encode(), address)
        print('Starting get Data')
        
        #call function to handle file data flow
        putHandler.rdtFileDataReceiver(fileName, s)
        
        break
    else:
        break
