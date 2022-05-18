import pickle
import hashlib
import sys
import socket

class FileSegment :
    def __init__(self, packetType, sequenceNumber, data, checksum):
        self.packetType = packetType
        self.sequenceNumber = sequenceNumber
        self.data = data
        self.checksum = checksum
        
        
def saveFile(fileName, serverSocket):
    
    #packet type constant, value 2 means that packets sent by the client will be ack packets
    
    packetType = 2
    
    #variable to trace packet sequence number to receive
    sequenceNumberToReceive = 1
    
    #buffer bytes to read
    BUFFER_SIZE = sys.getsizeof(FileSegment)
    
    # open file into write mode
    f = open('./upload/' + fileName, "wb")
    
    while True:
        
        serverSocket.settimeout(0.5)
        
        try:
           #receive packet from the client
           rawPacket, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            print('File transmission completed')
            f.close()
            return 1
        except socket.error as emsg:
            print("Socket recv error: ", emsg)
            
        print("rdt_recv: Received a message of size %d" % len(rawPacket))
        
        serverSocket.settimeout(None)
        
        #convert raw packet into FileSegment object
        packet = pickle.loads(rawPacket)
        
        #checksum controll
        if hashlib.md5(rawPacket).hexdigest() == packet.checksum: # check for checksum
            print("rdt_rcv: Recieved a corrupted packet: Type = DATA, Length = %d" % len(rawPacket))
            print("rdt_rcv: Drop the packet")
            
            #not send ack, so will receive the same packet
            continue
        if packet.packetType == 1:
            print("rdt_rcv: Got an expected Packet")
            if packet.sequenceNumber == sequenceNumberToReceive:
                
                #write packet data to file
                
                f.write(packet.data)
                
                #prepare ack packet
                
                ack = FileSegment(packetType, packet.sequenceNumber, '', 0)
                
                #calculate checksum
                ack.checksum = hashlib.md5(pickle.dumps(ack)).hexdigest()
                
                try:
                    #send ack fr just received packet
                    serverSocket.sendto(pickle.dumps(ack), clientAddress)
                except socket.error as emsg:
                    print("Socket send error: ", emsg)
                    return -1
                
                ++sequenceNumberToReceive
            else:
                
                #if received packet already received, send ack to client, 
                # maybe ack loss happened
                
                ack = FileSegment(packetType, packet.sequenceNumber, '', 0)
                
                #calculate checksum
                ack.checksum = hashlib.md5(pickle.dumps(ack)).hexdigest()
                
                try:
                    serverSocket.sendto(pickle.dumps(ack), clientAddress)
                except socket.error as emsg:
                    print("Socket send error: ", emsg)
                    return -1
        else:
            continue # if ack recieved in the first place then ignore
    
def sendFile(fileName, clientSocket, serverAddress):
    
    #set packet type to constant, 1 means that the packet contains file segment 
    packetType = 1
    
    #variable to trace packet sequence number to send
    sequenceNumberToSend = 1
    
    #buffer bytes to read
    BUFFER_SIZE = sys.getsizeof(FileSegment)
    
    ACK_TIMEOUT = 0.05
   
    #open file into read mode
    f = open(fileName, "rb") 
   
    #first file segment to send
    fileData = f.read(BUFFER_SIZE)
   
    while True:
        
        #prepare packet to send
        packet = FileSegment(packetType, sequenceNumberToSend, fileData, 0)
        
        if not fileData:
            # eof, close socket
            print('eof, closing socket')
            f.close()
            clientSocket.close()
        
        #calculate checksum 
        packet.checksum = hashlib.md5(pickle.dumps(packet)).hexdigest()
        
        try:
             #send the packet
             clientSocket.sendto(pickle.dumps(packet), serverAddress)
        except socket.error as emsg:
            print("Socket send error: ", emsg)
            return -1
        
        #set timout for ack
        clientSocket.settimeout(ACK_TIMEOUT) 
        
        try:
            #wait ack for packet just sent
            rawAck, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            print("rdt_send: Timeout!! Retransmit the packet %d again" % sequenceNumberToSend) 
            continue
        except socket.error as emsg:
            print("Socket recv error: ", emsg)
            
        clientSocket.settimeout(None) #end timer
        
        #convert raw ack packet into FileSegment object
        ack = pickle.loads(rawAck)
        
        #checksum controll
        if hashlib.md5(rawAck).hexdigest() == ack.checksum: # calculate the checksum
           print("rdt_send: Recieved a corrupted packet: Type = DATA, Length = %d" % len(rawAck))
           continue
        
        #checks if packet received is really an ack
        if ack.packetType == 2:
            print("rdt_send: Recieved the expected ACK")
            if ack.sequenceNumber == sequenceNumberToSend:
                #expected ack received, increment sequence number to send
                #and read next file segment
                ++sequenceNumberToSend
                fileData = f.read(BUFFER_SIZE)
            else:
                #not expected ack received, retransmit the packet
                continue