from socket import *
import json


def Data(Image, Command: str, Year: int, Month: int, Date: int, Hour: int, Min: int):
    Out = {
        "Image": Image,
        "Command": Command,
        "Year": Year,
        "Month": Month,
        "Date": Date,
        "Hour": Hour,
        "Min": Min
    }
    return json.dumps(Out).encode()


def Read(Client, BufferSize):
    BufferData = ""
    Size = None
    Request = "Init"
    while len(Request):
        Request = Client.recv(BufferSize).decode()
        BufferData += Request
        if Size is None:
            Size, BufferData = BufferData.split(Split, maxsplit=1)
            Size = int(Size)
        if Size - len(BufferData) <= 0:
            return BufferData.decode()
    return BufferData.decode()


Main = socket()

IP = "192.168.1.6"
Split = "-||-"
Port = 24682
Buffer = 1024 * 64


Break = "Break"

Mode1 = "Mode1"
Mode2 = "Mode2"

AnalyticsMode = True

# Main part

Main.connect((IP, Port))

while True:
    Command = Read(Main, Buffer)
    if AnalyticsMode:
        Main.send(Data("", "", 0, 0, 0, 0, 0))
        "Analytics part here"
    else:
        Main.send(Data("", "", 0, 0, 0, 0, 0))
        "Motion Detection part here"
    if Command == Mode1:
        AnalyticsMode = True
    elif Command == Mode2:
        AnalyticsMode = False
    elif Command == Break:
        break
    else:
        pass

Main.close()
