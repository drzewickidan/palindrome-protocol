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
                    elif str(cmd[0]) == "TOP":
                        if self.palindromes:
                            response = "%s" % self.palindromes[-1]
                        else:
                            response = "palindrome list is empty"
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
                        response = ""
                        for i in range(1, len(cmd)):
                            if self.is_palindrome(str(cmd[i])):
                                self.palindromes.append(str(cmd[i]))
                                response += str(cmd[i]) + " is a palindrome\n"
                            else:
                                response += str(cmd[i]) + " is not a palindrome\n"
                        response = response[:-1]  # remove extra newline
                    elif str(cmd[0]) == "QUIT":
                        self.close_client(client, address)
                        return False
                    else:
                        response = "unrecognized command"
                    client.send(response)
            except Exception as e:
                self.close_client(client, address)
                print e
                return False

    @staticmethod
    def close_client(client, address):
        print "closing connection to %s,%s" % (address[0], address[1])
        client.close()

    @staticmethod
    def is_palindrome(s):
        return s == s[::-1]


if __name__ == "__main__":
    ThreadedServer('127.0.0.1', 5000).listen()
