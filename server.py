import socket
import tempfile
import os

host = '127.0.0.1'
port = 5000


def server():
    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    c, addr = s.accept()

    # create palindrome file
    file("palindromes.txt", 'w')

    while True:
        with open('palindromes.txt', 'a+') as tmp:
            data = c.recv(1024)
            if not data:
                break
            rsp = ""
            cmd = data.split(' ')
            if str(cmd[0]) == "LIST":
                lines = tmp.readlines()
                for num, line in enumerate(lines, 1):
                    rsp += "%s %s" % (num, line)
                c.send(rsp[:-1])
            elif str(cmd[0]) == "RETR":
                # cmd[1] will be the int of which palindrome to return
                pass
            elif str(cmd[0]) == "QUIT":
                break
            elif is_palindrome(str(data)):
                tmp.write(str(data) + "\n")
                rsp = str(data) + " is a palindrome"
                c.send(rsp)
            else:
                rsp = str(data) + " is not a palindrome"
                c.send(rsp)
    c.close()
    os.remove('palindromes.txt')


def is_palindrome(s):
    return s == s[::-1]


if __name__ == "__main__":
    server()
