import socket
import sys

# address and port of server
# for ECEC531, this is hardcoded to run on localhost:5000
host = '127.0.0.1'
port = 5000


def client():
    # create client obeject
    s = socket.socket()
    s.connect((host, port))

    if len(sys.argv) == 2:
        # non-persistent connection
        if sys.argv[1] == "-np" or sys.argv[1] == "--non-persistent":
            # user input to send to server
            msg = raw_input()
            # check if QUIT command was used
            if not msg == "QUIT":
                # send command
                s.send(msg)
                # receive response from server
                data = s.recv(1024)
                # display data received from server
                print str(data)
            # if QUIT was entered, first tell the server to close connection and then close socket
            s.send("QUIT")
            s.close()
        else:
            raise Exception("unrecognized argument")
    elif len(sys.argv) > 2:
        # if the amount of arguments are greater than two (client.py <arg1> [<arg2>] raise an Exception)
        raise Exception("too many arguments")
    # default: persistent connection
    else:
        # user input to send to server
        msg = raw_input()
        while True:
            # if QUIT is entered, send to server and break loop to close connection
            if msg == "QUIT":
                s.send(msg)
                break
            # send command
            s.send(msg)
            # receive response from server
            data = s.recv(1024)
            # display data received from server
            print str(data)
            # continue sending commands
            msg = raw_input()
        s.close()

if __name__ == "__main__":
    client()
