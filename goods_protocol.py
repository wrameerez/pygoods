import struct
from datetime import datetime


class GCommand(object):
    """I send a command in GOODS protocol and receive its reply"""

    # Constants
    BUFFER_SZ = 16

    # Codes
    CMD_OK = 21

    def __init__(self, transport):
        self.command_buffer = bytearray(GCommand.BUFFER_SZ)
        self.reply_buffer = bytearray(GCommand.BUFFER_SZ)
        self.transport = transport

    def run(self):
        """Execute the command and listen to reply"""
        self.transport.send_data(self.command_buffer)
        self.send_command_data()
        self.transport.receive_fully_into(self.reply_buffer)
        return self.ran_ok()

    def command_code(self):
        pass

    def send_command_data(self):
        pass

    def set_command_message(self, command, a_byte, a_short, a_long1, a_long2):
        """Send all these numbers in network (big-endian) format"""
        struct.pack_into(">bbhll", self.command_buffer, 0,
                         command, a_byte, a_short, a_long1, a_long2)

    def set_command_with_long(self, a_long):
        self.set_command_message(self.command_code(), 0, 0, a_long, 0)

    def return_code(self):
        return self.reply_buffer[0]

    def ok_status(self):
        return self.__class__.CMD_OK

    def ran_ok(self):
        return self.return_code() == self.ok_status()


class GLoginCommand(GCommand):
    """Login command"""

    # Codes
    CMD_LOGIN = 17

    @classmethod
    def default_session_name(cls):
        """Makes up a unique session name"""
        return u'pygoods{0}'.format(str(datetime.now().microsecond))

    def __init__(self, transport, session_name=None):
        super().__init__(transport)
        if session_name:
            self.session_name = session_name
        else:
            self.session_name = self.__class__.default_session_name()
        self.set_command_with_long(len(self.session_name))

    def command_code(self):
        return self.__class__.CMD_LOGIN
    
    def send_command_data(self):
        self.transport.send_data(bytearray(self.session_name, 'utf-8'))

    def session_name(self):
        return self.session_name


class GLogoutCommand(GCommand):
    """Logout from GOODS session"""

    # Codes
    CMD_LOGOUT = 18
    CMD_BYE = 20

    def __init__(self, transport):
        super().__init__(transport)
        self.set_command_with_long(0)

    def ok_status(self):
        """For logout, ok status is cmd_bye not cmd_ok"""
        return self.__class__.CMD_BYE

    def command_code(self):
        return self.__class__.CMD_LOGOUT
