#client software
#using localhost server

#connect to server
import socket, sys
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket

print('Socket Created')

host = 'localhost'
port = 60006

try:
    remoteIP = socket.gethostbyname(host) #convert url to ip

except socket.gaierror:
    print('Could not be resolved. Try again') #deal with error
    sys.exit()

s.connect((remoteIP, port)) #connect to server

username = input('Username: ')
s.send(bytes(username, 'utf-8')) #send user info to server

print("Connected to server")

def listen():
    while 1:
        result = s.recv(1024).decode('utf-8') #receiver sender and file name
        print('\rReceived a thing!')
        print(result)
        if ':' in result:
            splitData = result.split(':') #0 is sender, 1 is file name, 2 is amount of lines
            invalid = True
            while invalid: #loop until answer is valid
                result = input("\rAccept file '" + splitData[1] + "' from " + splitData[0] + "? (y/n)").lower
                if (result == 'y'):
                    status = 'a'
                    invalid = False
                elif (result == 'n'):
                    status = 'd'
                    invalid = False
                else:
                    print('Invalid response')
                    invalid = True

            f = open(splitData[1])

            amountOfLines = s.recv(1024).decode('utf-8')
            linesReceived = 0
            while linesReceived <= amountOfLines:
                line = s.recv(1024)
                f.write(line)
                linesReceived = linesReceived + 1
                print(linesReceived)
        else:
            print(result)

            if(result == 'a'): #send file if its accepted
                print('Sending file')
                file = f.read(1024)
                passes = 1
                while (file): #read and send line by line
                    print((passes/totalPasses)*100 + '%', end="\r") #percent of progress counter
                    s.send(file)
                    file = f.read(1024)
                    passes = passes + 1

                print('File sent')
                f.close() #close file

            #tell them the file cant be sent for what ever reason
            elif(result == 'na'):
                print(eR + ' is not available.') 

            elif(result == 'd'):
                print(eR + ' declined your file.')

            elif(result == 'to'):
                print(eR + ' did not accept file in time') 
    
            elif(result == 'ue'):
                print('Unknown server error')

            elif(result == 'aa'):
                print(eR + ' is already transferring a file')


Thread(target=listen).start() #start lisntener on new thread


while 1:
    fileLoc = input('File path to send: ')    
    try:
        f = open(fileLoc)
    except (FileNotFoundError): #make sure file is accessible
        print('Invalid file location')
        raise

    fileName = fileLoc.split('/')[-1] #get file name

    totalPasses = sum(1 for line in f)

    eR = input('User to send to: ')
    s.send(bytes(eR + ':'+ fileName + ':' + str(totalPasses), 'utf-8')) #send file name and recipitent to server    