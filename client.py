import socket
import sys

#address and port of host
host = '127.0.0.1'
port = 5000


def client():
    #create connection client
    s = socket.socket()
    s.connect((host, port))
    
    #check amount of arguments
    if len(sys.argv) == 2:
        # non-persistent connection
        if sys.argv[1] == "-np" or sys.argv[1] == "--non-persistent":
            #save user input as msg
            msg = raw_input()
            #check if QUIT command was used
            if not msg == "QUIT":
                #send msg
                s.send(msg)
                #receive response from server
                data = s.recv(1024)
                #display data received from server
                print str(data)
            #if QUIT was entered, send to server and close connection
            s.send("QUIT")
            s.close()
        else:
            raise Exception("unrecognized argument")
    elif len(sys.argv) > 2:
        raise Exception("too many arguments")
    else:
        # default: persistent connection
        #use user input as msg
        msg = raw_input()
        while True:
            #if QUIT is entered, send to server and break loop to close connection
            if msg == "QUIT":
                s.send(msg)
                break
            #send msg
            s.send(msg)
            #receive response from server
            data = s.recv(1024)
            #display data received from server
            print str(data)
            msg = raw_input()
        s.close()

if __name__ == "__main__":
    client()
