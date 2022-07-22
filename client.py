
import socket
import os

import rdt_handler

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
putHandler = rdt_handler.RdtFileTransferHandler();

serverAddress = ('localhost', 10000)

initialMessage="ready"
uploadPath = os.getcwd()+"\\Upload\\"
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
    #send ready message to server
    socketUDP.sendto(initialMessage.encode(), serverAddress)
    
    #wait server's answer
    ready, address = socketUDP.recvfrom(4096)
    
    while(True):
        menu()
        choice=input("Choose[1..4]: ")
        #send choice to server
        socketUDP.sendto(choice.encode(), serverAddress)
        #wait server's answer
        ready, address = socketUDP.recvfrom(4096)
        
        if(choice == 1):
            #Print file list
            files = os.listdir(uploadPath)
            print(files)
        elif(choice == 2):
            #TODO controllo risposta del server 
            name=input("Insert file name to put: ")
            fileName = uploadPath + name
            putHandler.rdtFileDataSender(fileName, socketUDP, serverAddress)
        elif(choice == 3):
            #TODO controllo risposta del server
            name=input("Insert file name to get: ")
            fileName = downloadPath + name
            putHandler.rdtFileDataReceiver(fileName, socketUDP)
        elif(choice == 4): 
            print("exit...")
            break
        else:
            print("Wrong choice")
    
    # if(not os.path.exists(payload['fileName'])):
    #     print('File not exists')
    #     socketUDP.close()
    
except Exception as info:
    print(info)
finally: 
    print('closing socket')
    socketUDP.close()
    
