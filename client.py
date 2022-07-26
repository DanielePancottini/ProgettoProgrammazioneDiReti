
import socket
import os

import rdt_handler

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
putHandler = rdt_handler.RdtFileTransferHandler();

serverAddress = ('localhost', 10000)

uploadPath = os.getcwd()+"\\ToUpload\\"
downloadPath = os.getcwd()+"\\Download\\"

choice=-1
def menu():
    print("-------------------------")
    print("Welcome\n")
    print("1. File List")
    print("2. Put File")
    print("3. Get File")
    print("4. Exit")
    print("------------------------")    
    
 
try:
    
    
    while(True):
        menu()
        choice=input("Choose[1..4]: ")
        
        if(choice == '1'):
            #Send to server command for receive file's list
            socketUDP.sendto('list'.encode(), serverAddress)
            #receive files
            files, address = socketUDP.recvfrom(4096)
            print(files)
        elif(choice == '2'):
            name=input("Insert file name to put: ")
            fileName = uploadPath + name
            #Send to server command for put file
            socketUDP.sendto(('put '+ name).encode(), serverAddress)
            #Wait answer of server
            ok, address = socketUDP.recvfrom(4096)
            #Using rdt handler to manage packets
            rdt_handler.rdtFileDataSender(fileName, socketUDP, serverAddress)
        elif(choice == '3'):
            name=input("Insert file name to get: ")
            fileName = downloadPath + name
            #Send to server command for get file
            socketUDP.sendto(('get '+ name).encode(), serverAddress)
            ok, address = socketUDP.recvfrom(4096)
            #check file
            if(ok == 'ERROR FILENAME'):
                print("File name doesn't exist")
                socketUDP.close()
            #Using rdt handler to manage packets
            rdt_handler.rdtFileDataReceiver(fileName, socketUDP)
        elif(choice == '4'): 
            print("exit...")
            break
        else:
            print("Wrong choice")
    
except Exception as info:
    print(info)
finally: 
    print('closing socket')
    socketUDP.close()
    
