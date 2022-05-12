
import socket
import json

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverAddress = ('localhost', 10000)
message = 'list'

try:
    
    print('sending %s' % message)
    sent = socketUDP.sendto(message.encode(), serverAddress)
    data, address = socketUDP.recvfrom(4096)
    files = json.loads(data.decode())
    
    print(files[0])

except Exception as info:
    print(info)
finally: 
    print('closing socket')
    socketUDP.close()