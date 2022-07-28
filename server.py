
import socket
import os
import pickle

import rdt_handler

# udp server socket definition and binding
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 10000))

#welcome message
print('Server Running...')

# declaring RdtFileTransferHandler object to handle rdt file transfer transmission
# between client and server
rdtHandler = rdt_handler.RdtFileTransferHandler()
filesPath = './upload'

try: 
        
    while(True):
        
        # get command from client (list, put, get)
        rawCommandPacket, address = s.recvfrom(4096)
        print('Received Command: %s | From: %s' % (rawCommandPacket, address))
        
        # split command by other params
        commandPacket = rawCommandPacket.decode().split()
        command = commandPacket[0]
        
        #command switch for list, get, put
        if command.lower() == 'list':
            # send to client files list as array of strings
            files = os.listdir(filesPath)
            s.sendto(pickle.dumps(files), address)
            
        elif command.lower() == 'get':
            # check if file exists, if not send error, otherwise start rdt file transmission for get
            filename = commandPacket[1]
            if(os.path.exists(filesPath + '/' + filename) == False):
                s.sendto('ERROR FILENAME'.encode(), address)
                continue
            else:
                s.sendto('ACK GET'.encode(), address)
                rdtHandler.rdtFileDataSender(filesPath + '/' + filename, s, address)
        
        elif command.lower() == 'put':
            #send command ack and start rdt file transmission for put
            filename = commandPacket[1]
            s.sendto('PUT ACK'.encode(), address)
            rdtHandler.rdtFileDataReceiver(filesPath + '/' + filename, s)

except Exception as error:
    print(error)
    s.close()