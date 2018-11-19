import socket


host = '127.0.0.1'
port = 5000


def server():
    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    c, addr = s.accept()

    while True:
        data = c.recv(1024)
        if not data:
            break
        if is_palindrome(str(data)):
            data = str(data) + " is a palindrome"
        else:
            data = str(data) + " is not a palindrome"
        c.send(data)
    c.close()


def is_palindrome(s):
    return s == s[::-1]


if __name__ == "__main__":
    server()
