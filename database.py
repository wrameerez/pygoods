from goods_transports import GConnection


class GDatabase(object):

    def __init__(self, connection):
        self.connection = connection

    def connection(self):
        return self.connection

    @classmethod
    def opendb(cls, host='localhost', port=6100):
        """Use this factory method to create database instances"""
        return GConnection(host, port)

if __name__ == '__main__':
    database = GDatabase.opendb()
    database.login()
    database.logout()
