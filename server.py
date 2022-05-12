
import socket
import os
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 10000))

while(True):
    data, address = s.recvfrom(4096)
    print('received message from %s %s' % (data, address))
    # gestisce le alternative del menu e restituisce il messaggio di riferimento

    command = data.decode()

    if(command == 'list'):
        files = json.dumps(os.listdir('./upload'))
        s.sendto(files.encode(), address)
    elif(data == 'get'):
        break
    elif(data == 'put'):
        break
    else:
        break
