import json
from DataStore import InitDataset, GetTimely, YearlyReport, MonthlyReport, ClusteredMonthlyReport, DailyReport
from DataGenerator import Response, Header, Type, Report
import numpy as np
from Core import Init
import matplotlib.pyplot as plt

IP = "0.0.0.0"
Split = "-||-"
Buffer = 1024 * 64


class Mode:
    Analytics = "Model1"
    Intruder = "Model2"


CurrMode = Mode.Analytics


class WebSocketHandler:
    def __init__(self, WebSocket):
        self.__WebSocket = WebSocket

    async def send(self, Data):
        print(Data.decode())
        await self.__WebSocket.send(Data.decode())


def Parser(Strings):
    return f"{len(Strings)}{Split}{Strings}".encode()


def RequestHandler(Request):
    global CurrMode
    Out = Response(Header.Failure)
    if Request["Type"] == Type.All:
        Out = Response(Header.Success,
                       Report(GetTimely(Df), DailyReport(Df), MonthlyReport(Df), YearlyReport(Df),
                              ClusteredMonthlyReport(Df)))
    elif Request["Type"] == Type.SetType:
        CurrMode = Request["Other"]
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
            return Buffer
    return Buffer


def ImageProcessing(Client, Address):
    while True:
        Image = Read(Client, Buffer)
        Image = json.loads(Image)
        print(Image["Year"], Image["Month"], Image["Date"], Image["Hour"], Image["Min"])
        Img = np.array(Image["Image"])
        """
        Use the Image Here
        """
        Client.send(Parser(CurrMode))


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


Df = InitDataset()
Core = Init(IP)
Core.WebRequestProcessing = WebRequestProcessing
Core.TCPRequestProcessing = TCPPreprocessing
Core.TCPInputProcessing = ImageProcessing

Core.Start()
