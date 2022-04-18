from socket import *
import json

import numpy as np
from picamera import PiCamera
from datetime import datetime
import matplotlib.pyplot as plt


def Data(Image, Command, Year, Month, Date, Hour, Min):
    Out = {
        "Image": Image,
        "Command": Command,
        "Year": Year,
        "Month": Month,
        "Date": Date,
        "Hour": Hour,
        "Min": Min
    }
    return json.dumps(Out)


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
            return BufferData
    return BufferData


Main = socket()

IP = "192.168.111.40"
Split = "-||-"
Port = 24682
Buffer = 1024 * 64

Break = "Break"

Mode1 = "Mode1"
Mode2 = "Mode2"

AnalyticsMode = True
CameraUsage = False

# Main part

Main.connect((IP, Port))
camera = PiCamera()

camera.resolution = (250, 250)
camera.framerate = 30


class CameraOut:
    def __init__(self):
        self.size = 0

    def write(self, s):
        self.size += len(s)
        print(s)

    def flush(self):
        print('%d bytes would have been written' % self.size)


def Parser(String):
    return f"{len(String)}{Split}{String}".encode()


CameraObj = CameraOut()


def InitCamera():
    global CameraUsage
    if not CameraUsage:
        camera.start_recording(CameraObj)
        CameraUsage = True


def CloseCamera():
    global CameraUsage
    if CameraUsage:
        camera.stop_recording()
        CameraUsage = False


while True:
    if AnalyticsMode:
        InitCamera()
        Img = np.zeros((100, 100, 3))
        Time = datetime.now()
        Main.send(Parser(Data(Img.tolist(), "", Time.year, Time.month, Time.day, Time.hour, Time.minute)))
    else:
        CloseCamera()
        Main.send(Data("", "", 0, 0, 0, 0, 0))
        "Motion Detection part here"
    Command = Read(Main, Buffer)
    print(Command)
    if Command == Mode1:
        AnalyticsMode = True
    elif Command == Mode2:
        AnalyticsMode = False
    elif Command == Break:
        break
    else:
        pass

Main.close()
