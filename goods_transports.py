import socket
from goods_protocol import *


class GTransport(object):
    """I am an abstract GOODS transport base class"""

    def send_data(self, a_byte_array):
        pass

    def receive_fully_into(self, a_byte_array):
        pass


class GTCPTransport(GTransport):
    """I am a TCP/IP transport to GOODS"""

    def __init__(self, host='localhost', port=6100):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_data(self, a_byte_array):
        self.socket.sendall(a_byte_array)

    def receive_fully_into(self, a_byte_array):
        self.socket.recv_into(a_byte_array)


class GConnection(object):
    """I am a GOODS database connection API facade"""

    @classmethod
    def default_transport_class(cls):
        """By default connect using TCP transport"""
        return GTCPTransport

    @classmethod
    def transport_to(cls, host, port):
        """Return an instance of the connection transport to the server"""
        return cls.default_transport_class()(host, port)

    def __init__(self, host='localhost', port=6100):
        self.transport = self.__class__.transport_to(host, port)

    def login(self, session_name=None):
        command = GLoginCommand(self.transport, session_name)
        if command.run():
            print("Logged in")
        else:
            print("Error:", command.return_code())

    def logout(self):
        command = GLogoutCommand(self.transport)
        if command.run():
            print("Logged out")
        else:
            print("Error:", command.return_code())

