import struct
from datetime import datetime

class GCommand(object):
    "I send a command in GOODS protocol and receive its reply"

    # Constants
    BUFFER_SZ = 16

    # Codes
    CMD_OK = 21


    def __init__(self, transport):
        self.commandBuffer = bytearray(GCommand.BUFFER_SZ)
        self.replyBuffer = bytearray(GCommand.BUFFER_SZ)
        self.transport = transport

    def run(self):
        "Execute the command and listen to reply"
        self.transport.sendData(self.commandBuffer)
        self.sendCommandData()
        self.transport.receiveFullyInto(self.replyBuffer)
        return self.ranOk()

    def commandCode(self):
        pass

    def sendCommandData(self):
        pass

    def setCommandMessage(self, command, aByte, aShort, aLong1, aLong2):
        "Send all these numbers in network (big-endian) format"
        struct.pack_into(">bbhll", self.commandBuffer, 0,
                command, aByte, aShort, aLong1, aLong2)    

    def setCommandWithLong(self, aLong):
        self.setCommandMessage(self.commandCode(), 0, 0, aLong, 0)

    def returnCode(self):
        return self.replyBuffer[0]

    def ranOk(self):
        return self.returnCode == self.__class__.CMD_OK



class GLoginCommand(GCommand):
    "Login command"

    # Codes
    CMD_LOGIN = 17

    @classmethod
    def defaultSessionName(cls):
        "Makes up a unique session name"
        return 'pygoods' + str(datetime.now().microsecond)

    def __init__(self, transport, sessionName=None):
        super().__init__(transport)
        if sessionName:
            self.sessionName = sessionName
        else:
            self.sessionName = self.__class__.defaultSessionName()
        self.setCommandWithLong(len(self.sessionName))

    def commandCode(self):
        return self.__class__.CMD_LOGIN
    
    def sendCommandData(self):
        self.transport.sendData(bytearray(self.sessionName, 'utf-8'))

    def sessionName(self):
        return self.sessionName
