import socket, sys, time, select
from threading import Thread

HOST = ''
PORT = 80085

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
        c = allConn(index) #get their socket

        allCon[c].send(bytes(senderName + ':' + file, 'utf-8'))
        ready = select.select([s], [], [], 120) #waits 120 seconds for a response
        if ready[0]:
            result = allCon[c].recv(1024)
        else:
            status = 'to' #to for timeout

        if (result == 'a'): #a for accept
            status = 'a'
        elif (result == 'd'): #d for decline
            status = 'd'
        
    return status

def clientThread(conn): #what the client talks to
    sender = conn.recv(1024) #client username
    online.append(sender) #add to online list
    while True:
        active.append(sender)#mark them as active
        eRaF = conn.recv(1024).split(':') #eRaF is end receiver and file, split by :
        eR = eRaF(0)
        fileName = eRaF(1)
        eRStatus = accept(sender, conn, eR, fileName) #check if user can receive file
        conn.send(bytes(eRStatus)) #send user the status
                
    conn.close()

while 1:
    conn, addr = s.accept() #accept incoming connections
    allConn.append(conn) #add to connected sockets
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    Thread(target=clientThread, args=(conn)).start() #start clientThread on new thread

s.close()