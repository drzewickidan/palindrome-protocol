import socket
import threading


class ThreadedServer(object):
    """A TCP server that listens to multiple clients

    When a new client attempts to connect, this class will create a new thread to listen and respond
    to that particular client. Each client can send the following commands:
        VRFY <word> [<word> ...] : verifies whether a word is a palindrome or multiple words are palindromes
        LIST : return a list of palindromes found including the palindromes other clients have found
        TOP : return the last palindrome found
        RETR <#> : return a particular palindrome from the LIST command
        STAT : return the number of palindromes found
        DELE <#> : remove a particular palindrome from the LIST command
        REST : reset the list of palindromes
        QUIT : end the session with the server

    """

    def __init__(self, host, port):
        """Initializes ThreadedServer

        Binds a TCP socket to an IP and port and initializes a list of palindromes that each thread shares

        :param host: Host IP address in the form a.b.c.d
        :param port: Host port to accept connections from clients

        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.palindromes = []

    def listen(self):
        """Listen for new clients trying to connect and spawn a thread to listen to their commands"""
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):
        """Listen for commands from a particular client
        :param client: socket object usable to send and receive data on the connection
        :param address: address bound to the socket on the other end of the connection

        """
        # print welcome message to indicate which client this thread is listening to
        print "connection established to %s,%s" % (address[0], address[1])
        while True:
            try:
                # attempt to receive data
                data = client.recv(1024)
                if data:
                    cmd = data.split(' ')
                    # check if list was requested
                    if str(cmd[0]) == "LIST":
                        if self.palindromes:
                            response = ""
                            # add each item in palindrome list to response
                            for num, line in enumerate(self.palindromes, 1):
                                response += "%s %s\n" % (num, line)
                            # remove extra newline
                            response = response[:-1]
                        else:
                            response = "palindrome list is empty"
                    # returns palindrome at specified index upon receiving RETR command
                    elif str(cmd[0]) == "RETR":
                        if int(cmd[1]) - 1 < len(self.palindromes) and not int(cmd[1]) <= 0:
                            response = str(self.palindromes[int(cmd[1])-1])
                        else:
                            response = "palindrome %s does not exist" % str(cmd[1])
                    # returns last palindrome found when TOP command received
                    elif str(cmd[0]) == "TOP":
                        if self.palindromes:
                            response = "%s" % self.palindromes[-1]
                        else:
                            response = "palindrome list is empty"
                    # clear palindrome at specified position when DELE command received
                    elif str(cmd[0]) == "DELE":
                        if int(cmd[1]) - 1 < len(self.palindromes) and not int(cmd[1]) <= 0:
                            del self.palindromes[int(cmd[1])-1]
                            response = "deleted palindrome %s" % str(cmd[1])
                        else:
                            response = "palindrome %s does not exist" % str(cmd[1])
                    # clear list of palindromes when RSET command received
                    elif str(cmd[0]) == "RSET":
                        self.palindromes = []
                        response = "reset list of palindromes"
                    # indicate number of palindromes found when STAT command received
                    elif str(cmd[0]) == "STAT":
                        if len(self.palindromes) == 1:
                            response = "1 palindrome found"
                        else:
                            response = "%s palindromes found" % len(self.palindromes)
                    # check for palindrome when VRFY command received
                    elif str(cmd[0]) == "VRFY":
                        # dynamically verify each word that the client sends
                        response = ""
                        for i in range(1, len(cmd)):
                            if self.is_palindrome(str(cmd[i])):
                                self.palindromes.append(str(cmd[i]))
                                response += str(cmd[i]) + " is a palindrome\n"
                            else:
                                response += str(cmd[i]) + " is not a palindrome\n"
                        # remove extra newline
                        response = response[:-1]
                    # close connection upon QUIT command
                    elif str(cmd[0]) == "QUIT":
                        self.close_client(client, address)
                        return False
                    else:
                        response = "unrecognized command"
                    # send response back to client
                    client.send(response)
            except Exception as e:
                self.close_client(client, address)
                print e
                return False

    @staticmethod
    def close_client(client, address):
        """Close a socket and print exit message"""
        print "closing connection to %s,%s" % (address[0], address[1])
        client.close()

    @staticmethod
    def is_palindrome(s):
        """Return whether a string is a palindrome or not"""
        return s == s[::-1]


if __name__ == "__main__":
    # executed when server module is run directly
    # for ECEC531, this is hardcoded to run on localhost:5000
    ThreadedServer('127.0.0.1', 5000).listen()
