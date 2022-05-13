
import socket
import time

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
    
    #start sending file data
    f = open(filename, "rb")
    
    while True:
        # read the bytes from the file
        bytes_read = f.read(4096)
        if not bytes_read:
            # eof
            print('eof')
            socketUDP.sendto('FILE END'.encode(), address)
            break
        
        socketUDP.sendto(bytes_read, address)
        
        #wait file segment ack before to continue sending
        socketUDP.recvfrom(4096)

except Exception as info:
    print(info)
finally: 
    print('closing socket')
    socketUDP.close()