
import socket

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverAddress = ('localhost', 10000)
command = 'put'
filename = 'caro.txt'

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
            socketUDP.sendto('FILE END'.encode(), address)
            break
        
        socketUDP.sendto(bytes_read, address)

except Exception as info:
    print(info)
finally: 
    print('closing socket')
    socketUDP.close()