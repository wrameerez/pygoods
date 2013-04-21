import socket
import struct
from datetime import datetime

class GTransport(object):

    def sendData(self, aByteArray):
        pass

class GTCPTransport(GTransport):

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        print("Connected to GOODS server.")

    def sendData(self, aByteArray):
        #print("Sending", type(aByteArray), aByteArray)
        self.socket.sendall(aByteArray)

    def receiveFullyInto(self, aByteArray):
        self.socket.recv_into(aByteArray)
        #print("Reply", aByteArray)



class GConnection(object):

    # Constants
    BUFFER_SZ = 16

    # Commands
    INVALID = 4
    LOGIN = 17
    OK = 21
    REFUSED = 22

    @classmethod
    def defaultTransportClass(cls):
        "By default connect using TCP transport"
        return GTCPTransport

    @classmethod
    def transportTo(cls, host, port):
        "Return an instance of the connection transport to the server"
        return cls.defaultTransportClass()(host, port)

    @classmethod
    def defaultSessionName(cls):
        "Makes up a unique session name"
        return 'pygoods' + str(datetime.now().microsecond)

    def __init__(self, host='localhost', port=6100, sessionName=None):
        self.transport = self.__class__.transportTo(host, port)
        self.headerBuf = bytearray(GConnection.BUFFER_SZ)
        if sessionName:
            self.sessionName = sessionName
        else:
            self.sessionName = self.__class__.defaultSessionName()
        self.login()

    def login(self):
        self.sendCommandWithLong(self.__class__.LOGIN, len(self.sessionName))
        self.sendData(self.sessionName)
        self.receiveOkOrRefused()
        print("Logged in")

    def sendCommandWithLong(self, command, aLong):
        self.sendCommand(command, 0, 0, aLong, 0)

    def sendCommand(self, command, aByte, aShort, aLong1, aLong2):
        "Send all these numbers in network (big-endian) format"
        struct.pack_into(">bbhll", self.headerBuf, 0,
                command, aByte, aShort, aLong1, aLong2)    
        self.sendData(self.headerBuf)

    def sendData(self, aByteArray):
        self.transport.sendData(aByteArray)

    def receiveOkOrRefused(self):
        self.receiveHeader()
        cmd = self.headerCommand()
        return cmd == self.__class__.OK

    def receiveHeader(self):
        self.receiveIntoHeaderBuffer()
        if self.headerCommand() == self.__class__.INVALID:
            print("Invalid response")
            self.receiveInvalid()
            self.receiveHeader()

    def receiveIntoHeaderBuffer(self):
        self.transport.receiveFullyInto(self.headerBuf)

    def receiveInvalid(self):
        pass

    def headerCommand(self):
        return self.headerBuf[0]

