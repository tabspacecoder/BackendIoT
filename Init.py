import json
from DataGenerator import Response, Header

from Core import Init

IP = "192.168.1.6"
Split = "-||-"
Core = Init(IP)
Buffer = 1024 * 64


class WebSocketHandler:
    def __init__(self, WebSocket):
        self.__WebSocket = WebSocket

    async def send(self, Data):
        print(Data.decode())
        await self.__WebSocket.send(Data.decode())


def Parser(Strings):
    return f"{len(Strings)}{Split}{Strings}".encode()


def RequestHandler(Request):
    Out = Response(Header.Success, Request)
    return Parser(Out)


def Read(Client, BufferSize):
    Buffer = ""
    Size = None
    Request = "Init"
    while len(Request):
        Request = Client.recv(BufferSize).decode()
        Buffer += Request
        if Size is None:
            Size, Buffer = Buffer.split(Split, maxsplit=1)
            Size = int(Size)
        if Size - len(Buffer) <= 0:
            return Buffer.decode()
    return Buffer.decode()


def ImageProcessing(Client, Address):
    Image = Read(Client, Buffer)
    """
    Write the Image processing here
    """


def TCPPreprocessing(Client, Address):
    Data = Read(Client, Buffer)
    Size, Data = Data.split(Split, maxsplit=1)
    Data = json.loads(Data)
    Out = RequestHandler(Data)
    Client.send(Out)


async def WebRequestProcessing(WebSocket, Path):
    Data = await WebSocket.recv()
    Client = WebSocketHandler(WebSocket)
    Size, Data = Data.split(Split, maxsplit=1)
    Data = json.loads(Data)
    Out = RequestHandler(Data)
    await Client.send(Out)


Core.WebRequestProcessing = WebRequestProcessing
Core.TCPRequestProcessing = TCPPreprocessing
Core.TCPInputProcessing = ImageProcessing

Core.Start()
