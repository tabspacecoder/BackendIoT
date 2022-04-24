from socket import *
from Thread import Thread
import mysql.connector
import asyncio
import websockets


DatabaseUser = "root"
DatabasePassword = "rootcore@123"
DatabaseHost = "127.0.0.1"
DatabasePort = 3306


def Pass(Client, Address):
    pass


class Init:
    def __init__(self, HostIP: str, OutgoingWebPort: int = 13579, OutgoingTCPPort: int = 24680,
                 IncomingTCPPort: int = 24682, Devices: int = 100, Buffer: int = 1024 * 64):
        self.Cursor = None
        self.Database = None
        self.__IncomingTCPThread = None
        self.__OutgoingTCPThread = None

        self.__IP = HostIP
        self.__OutgoingTCPPort = OutgoingTCPPort
        self.__IncomingTCPPort = IncomingTCPPort
        self.__OutgoingWebPort = OutgoingWebPort

        self.__Devices = Devices
        self.__Thread = None
        self.__Status = False
        self._IncomingSocket = None
        self._OutgoingSocket = None
        self.BufferSize = Buffer

        self.TCPRequestProcessing = Pass
        self.WebRequestProcessing = Pass

        self.TCPInputProcessing = Pass

        self.__BindThread = None
        self.__WebSocket = None
        self.__InitDatabase()

    def Start(self):
        self.__IncomingTCPThread = Thread(target=self.__InitIncomingTCP)
        self.__IncomingTCPThread.start()
        self.__OutgoingTCPThread = Thread(target=self.__InitOutgoingTCP)
        self.__OutgoingTCPThread.start()
        self.__InitOutgoingWebSocket()

    def __InitDatabase(self):
        print("Initializing database")
        self.Database = mysql.connector.connect(host=DatabaseHost, user=DatabaseUser, password=DatabasePassword,
                                                port=DatabasePort, database="DataManagement")
        self.Cursor = self.Database.cursor(buffered=True)
        print("Database initialized")

    def __InitOutgoingTCP(self):
        print("TCP outgoing initializing")
        self._OutgoingSocket = socket(AF_INET, SOCK_STREAM)
        self._OutgoingSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._OutgoingSocket.bind((self.__IP, self.__OutgoingTCPPort))
        self._OutgoingSocket.listen(self.__Devices),
        self.__Status = True
        print("TCP outgoing initialized")
        while True:
            Client, Address = self._OutgoingSocket.accept()
            thread = Thread(target=self.TCPRequestProcessing, args=(Client, Address))
            thread.Bind(self.__Thread)
            thread.start()

    def __InitIncomingTCP(self):
        print("TCP incoming initializing")
        self._IncomingSocket = socket(AF_INET, SOCK_STREAM)
        self._IncomingSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._IncomingSocket.bind((self.__IP, self.__IncomingTCPPort))
        self._IncomingSocket.listen(self.__Devices)
        self.__Status = True
        print("TCP incoming initialized")
        while True:
            Client, Address = self._IncomingSocket.accept()
            print(Address)
            thread = Thread(target=self.TCPInputProcessing, args=(Client, Address))
            thread.Bind(self.__Thread)
            thread.start()

    def __InitOutgoingWebSocket(self):
        print("Websocket initializing")
        self.__WebSocket = websockets.serve(self.WebRequestProcessing, self.__IP, self.__OutgoingWebPort)
        print("Websocket initialized")
        asyncio.get_event_loop().run_until_complete(self.__WebSocket)
        asyncio.get_event_loop().run_forever()
