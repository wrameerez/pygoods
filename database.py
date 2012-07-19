from goods_transports import GConnection

class GDatabase(object):

    @classmethod
    def opendb(cls, host='localhost', port=6100):
        instance= cls()
        print("Creating connection")
        instance.connection = GConnection(host, port)
        return instance

if __name__ == '__main__':
    GDatabase.opendb()
