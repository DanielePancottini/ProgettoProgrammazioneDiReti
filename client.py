
import socket

import putHandler

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverAddress = ('localhost', 10000)
command = 'put'
filename = 'grande.txt'

try:
    
    print('sending put command')
    sent = socketUDP.sendto(command.encode(), serverAddress)
    
    #wait for PUT ACK
    ready, address = socketUDP.recvfrom(4096)
    
    #send filename
    socketUDP.sendto(filename.encode(), address)
    
    #wait for filename ack
    ready, address = socketUDP.recvfrom(4096)
    
    putHandler.rdtFileDataSender(filename, socketUDP, serverAddress)

except Exception as info:
    print(info)
finally: 
    print('closing socket')
    socketUDP.close()