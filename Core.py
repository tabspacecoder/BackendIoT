from socket import *
from Thread import Thread
import asyncio
import websockets


def Pass(Client, Address):
    pass


class Init:
    def __init__(self, HostIP: str, OutgoingWebPort: int = 13579, OutgoingTCPPort: int = 24680,
                 IncomingTCPPort: int = 24682, Devices: int = 100, Buffer: int = 1024 * 64):
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

    def Start(self):
        self.__IncomingTCPThread = Thread(target=self.__InitIncomingTCP)
        self.__IncomingTCPThread.start()
        self.__OutgoingTCPThread = Thread(target=self.__InitOutgoingTCP)
        self.__OutgoingTCPThread.start()
        self.__InitOutgoingWebSocket()

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
        self._IncomingSocket.bind((self.__IP, self.__OutgoingTCPPort))
        self._IncomingSocket.listen(self.__Devices)
        self.__Status = True
        print("TCP incoming initialized")
        while True:
            Client, Address = self._IncomingSocket.accept()
            thread = Thread(target=self.TCPRequestProcessing, args=(Client, Address))
            thread.Bind(self.__Thread)
            thread.start()

    def __InitOutgoingWebSocket(self):
        print("Websocket initializing")
        self.__WebSocket = websockets.serve(self.WebRequestProcessing, self.__IP, self.__OutgoingWebPort)
        print("Websocket initialized")
        asyncio.get_event_loop().run_until_complete(self.__WebSocket)
        asyncio.get_event_loop().run_forever()
