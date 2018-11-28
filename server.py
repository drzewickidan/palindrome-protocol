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
                    response = ""
                    if str(cmd[0]) == "LIST":
                        for num, line in enumerate(self.palindromes, 1):
                            response += "%s %s\n" % (num, line)
                        response = response[:-1]  # remove extra newline
                    elif str(cmd[0]) == "RETR":
                        response = str(self.palindromes[int(cmd[1])-1])
                        #print self.palindromes[int(cmd[1])]
                        # cmd[1] will be the int of which palindrome to return
                        pass
                    elif str(cmd[0]) == "DELE":
                        pass
                    elif self.is_palindrome(str(data)):
                        self.palindromes.append(str(data))
                        response = str(data) + " is a palindrome"
                    else:
                        response = str(data) + " is not a palindrome"
                    client.send(response)
                else:
                    print "closing connection to %s,%s" % (address[0], address[1])
                    break
            except Exception:
                client.close()
                return False

    @staticmethod
    def is_palindrome(s):
        return s == s[::-1]


if __name__ == "__main__":
    ThreadedServer('127.0.0.1', 5000).listen()
