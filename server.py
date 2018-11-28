import socket
import threading


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.palindromes = []

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):
        print "connection established to %s,%s" % (address[0], address[1])
        while True:
            try:
                data = client.recv(1024)
                if data:
                    cmd = data.split(' ')
                    if str(cmd[0]) == "LIST":
                        if self.palindromes:
                            response = ""
                            for num, line in enumerate(self.palindromes, 1):
                                response += "%s %s\n" % (num, line)
                            response = response[:-1]  # remove extra newline
                        else:
                            response = "palindrome list is empty"
                    elif str(cmd[0]) == "RETR":
                        if int(cmd[1]) - 1 < len(self.palindromes) and not int(cmd[1]) <= 0:
                            response = str(self.palindromes[int(cmd[1])-1])
                        else:
                            response = "palindrome %s does not exist" % str(cmd[1])
                    elif str(cmd[0]) == "DELE":
                        if int(cmd[1]) - 1 < len(self.palindromes) and not int(cmd[1]) <= 0:
                            del self.palindromes[int(cmd[1])-1]
                            response = "deleted palindrome %s" % str(cmd[1])
                        else:
                            response = "palindrome %s does not exist" % str(cmd[1])
                    elif str(cmd[0]) == "RSET":
                        self.palindromes = []
                        response = "reset list of palindromes"
                    elif str(cmd[0]) == "STAT":
                        if len(self.palindromes) == 1:
                            response = "1 palindrome found"
                        else:
                            response = "%s palindromes found" % len(self.palindromes)
                    elif str(cmd[0]) == "VRFY":
                        if self.is_palindrome(str(cmd[1])):
                            self.palindromes.append(str(cmd[1]))
                            response = str(cmd[1]) + " is a palindrome"
                        else:
                            response = str(cmd[1]) + " is not a palindrome"
                    elif str(cmd[0]) == "QUIT":
                        print "closing connection to %s,%s" % (address[0], address[1])
                        break
                    else:
                        response = "unrecognized command"
                    client.send(response)
            except Exception:
                client.close()
                return False

    @staticmethod
    def is_palindrome(s):
        return s == s[::-1]


if __name__ == "__main__":
    ThreadedServer('127.0.0.1', 5000).listen()
