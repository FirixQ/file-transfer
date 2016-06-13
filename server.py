import socket, sys, time, select
from threading import Thread

HOST = ''
PORT = 80085

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
print('Socket created')

try:
    s.bind((HOST, PORT))
except socket.error:
    print('Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')

s.listen(10)
print('Socket listening')

allConn = []
active = []
online = []

def accept(senderName, senderAddr, receiver, file):
    if receiver in active:
        status = 'aa'
    elif receiver in online:
        index = online.index(receiver)
        c = allConn(index)

        allCon[c].send(bytes(senderName + ':' + file, 'utf-8'))
        
        result = allCon[c].recv(1024)

        if (result == 'a'):
            status = 'a'
        elif (result == 'd'):
            status = 'd'
        
    return status

def clientThread(conn):
    sender = conn.recv(1024)
    online.append(sender)
    while True:
        active.append(sender)
        eRaF = conn.recv(1024).split(':')
        eR = eRaF(0)
        fileName = eRaF(1)
        eRStatus = accept(sender, conn, eR, fileName)
        conn.send(bytes(eRStatus))
                
    conn.close()

while 1:
    conn, addr = s.accept()
    allConn.append(conn)
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    Thread(target=clientThread, args=(conn)).start()

s.close()