
import socket
import os
import json

import putHandler

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 10000))

while(True):
    
    #get command from client
    data, address = s.recvfrom(4096)
    print('received message from %s %s' % (data, address))
    
    command = data.decode()
    
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
        s.sendto('PUT ACK'.encode(), address)
        
        #receive filename to upload
        fileName, address = s.recvfrom(4096)
        print('Received filename')
        
        #if file already exists, close connection
        
        #send to client filename ack to receive file data
        s.sendto('FILENAME ACK'.encode(), address)
        print('Starting get Data')
        
        #call function to handle file data flow
        putHandler.rdtFileDataReceiver(fileName.decode(), s)
        
        break
    else:
        break
