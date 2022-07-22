
import socket

import rdt_handler

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
putHandler = rdt_handler.RdtFileTransferHandler();

serverAddress = ('localhost', 10000)

try:
    
   socketUDP.sendto('put PROVA.txt'.encode(), serverAddress);
    
   data, address = socketUDP.recvfrom(4096);
   
   putHandler.rdtFileDataSender('PROVA.txt', socketUDP, serverAddress);
    
except Exception as info:
    print(info)
finally: 
    print('closing socket')
    socketUDP.close()