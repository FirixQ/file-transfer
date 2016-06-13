#client software
#using localhost server

#connect to server
import socket, sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket

print('Socket Created')

host = 'localhost'
port = 80085

try:
    remoteIP = socket.gethostbyname(host) #convert url to ip

except socket.gaierror:
    print('Could not be resolved. Try again') #deal with error
    sys.exit()

s.connect((remoteIP, port))

username = input('Username: ')
s.send(bytes(username, 'utf-8'))

print("Connected to server")

while 1:
        
    try:
        fileLoc = input('File path to send: ')
        f = open(fileLoc)
    except (FileNotFoundError, IOError):
        print('Invalid file location')
        raise

    fileName = fileLoc.split('/')[-1]

    eR = input('User to send to: ')
    s.send(bytes(eR + ':'+ fileName, 'utf-8'))

    eRStatus = s.recv(1024).decode('utf8')

    if(eRStatus == 'a'):
        print('Sending file')
        file = f.read(1024)
        passes = 1
        while (file):
            print('Pass: ' + passes)
            s.send(file)
            file = f.read(1024)
            passes = passes + 1

        print('File sent')

    elif(eRStatus == 'nc'):
        print(eR + ' is not available.')

    elif(eRStatus == 'd'):
        print(eR + ' declined your file.')

    elif(eRStatus == 'to'):
        print(eR + ' did not accept file in time')   