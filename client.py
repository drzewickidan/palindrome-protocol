import socket


host = '127.0.0.1'
port = 5000


def client():
    s = socket.socket()
    s.connect((host, port))

    msg = raw_input()
    while msg != "quit":
        s.send(msg)
        data = s.recv(1024)
        print str(data)
        msg = raw_input()
    s.close()

if __name__ == "__main__":
    client()
