import socket
import sys

host = '127.0.0.1'
port = 5000


def client():
    s = socket.socket()
    s.connect((host, port))

    if len(sys.argv) > 1:
        # non-persistent connection
        if sys.argv[1] == "-np" or sys.argv[1] == "--non-persistent":
            msg = raw_input()
            if not msg == "QUIT":
                s.send(msg)
                data = s.recv(1024)
                print str(data)
            s.send("QUIT")
            s.close()
    else:
        # default: persistent connection
        msg = raw_input()
        while True:
            if msg == "QUIT":
                s.send(msg)
                break
            s.send(msg)
            data = s.recv(1024)
            print str(data)
            msg = raw_input()
        s.close()

if __name__ == "__main__":
    client()
