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

s.connect((remoteIP, port)) #connect to server

username = input('Username: ')
s.send(bytes(username, 'utf-8')) #send user info to server

print("Connected to server")

while 1:
        
    try:
        fileLoc = input('File path to send: ')
        f = open(fileLoc)
    except (FileNotFoundError, IOError): #make sure file is accessible
        print('Invalid file location')
        raise

    fileName = fileLoc.split('/')[-1] #get file name

    eR = input('User to send to: ')
    s.send(bytes(eR + ':'+ fileName, 'utf-8')) #send file name and recipitent to server

    eRStatus = s.recv(1024).decode('utf8') #get receiver status from server

    if(eRStatus == 'a'): #send file if its accepted
        print('Sending file')
        file = f.read(1024)
        passes = 1
        while (file): #read and send line by line
            print('Pass: ' + passes) #passes is basically a line counter. sorta like a progress counter
            s.send(file)
            file = f.read(1024)
            passes = passes + 1

        print('File sent')
        f.close() #close file

    #tell them the file cant be sent for what ever reason
    elif(eRStatus == 'nc'):
        print(eR + ' is not available.') 

    elif(eRStatus == 'd'):
        print(eR + ' declined your file.')

    elif(eRStatus == 'to'):
        print(eR + ' did not accept file in time')   