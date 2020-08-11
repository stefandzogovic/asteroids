import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1' # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        self.port = 9000
        self.addr = (self.host, self.port)
        self.connect()
        self.id = 0

    def connect(self):
        self.client.connect_ex(self.addr)

    def recv_pickle(self):
        try:
            reply = self.client.recv(2048)
            return reply
        except socket.error as e:
            return str(e)

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)

    def send2(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            return str(e)

    def recv(self):
        reply = self.client.recv(2048).decode()
        return reply