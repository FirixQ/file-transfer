import socket, sys, time, select
from threading import Thread

HOST = ''
PORT = 60006

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
print('Socket created')

try:
    s.bind((HOST, PORT)) #bind to port
except socket.error:
    print('Bind failed.')
    sys.exit() #quit on fail
     
print('Socket bind complete')

s.listen(10) #wait for connections
print('Socket listening')

allConn = [] #list all connected - socket
online = [] #list all connect - username (same index as allCon)
active = [] #list everyone uploading/downloading

def accept(senderName, senderAddr, receiver, file):

    if receiver in active: #check if receiver is currently doing something
        status = 'aa'
    elif receiver in online: #check if they are online
        index = online.index(receiver)
        c = allConn[index] #get their socket

        filenameInBytes = bytes(':' + file, 'utf-8') #some bytes magic
        c.send(senderName + filenameInBytes)
        ready = select.select([c], [], [], 120) #waits 120 seconds for a response
        if ready[0]:
            result = allCon[c].recv(1024)
        else:
            result = 'to' #to stop assignment errors

        if (result == 'a'): #a for accept
            status = 'a'
        elif (result == 'd'): #d for decline
            status = 'd'
        elif (result == 'to'):
            status = 'to'
        else:
            status = 'ue' #unknown error
    
    else:
        status = 'na' #not available

    return status

def clientThread(conn): #what the client talks to
    sender = conn.recv(1024) #client username
    online.append(sender.decode('utf-8')) #add to online list
    while True:
        eRaF = conn.recv(1024).decode('utf-8').split(':') #eRaF is end receiver and file, split by colon
        active.append(sender.decode('utf-8'))#mark them as active
        eR = eRaF[0]
        fileName = eRaF[1]
        eRStatus = accept(sender, conn, eR, fileName) #check if user can receive file
        conn.send(bytes(eRStatus, 'utf-8')) #send user the status
        print('About to receive file from ' + addr[0] + '(' + sender.decode('utf-8') + ')')
                
    conn.close()

while 1:
    conn, addr = s.accept() #accept incoming connections
    allConn.append(conn) #add to connected sockets
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    Thread(target=clientThread, args=(conn,)).start() #start clientThread on new thread

s.close()