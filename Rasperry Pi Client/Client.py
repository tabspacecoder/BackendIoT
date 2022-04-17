from socket import *
import json
# from picamera import PiCamera
from datetime import datetime
import matplotlib.pyplot as plt


def Parser(Strings):
    return f"{len(Strings)}{Split}{Strings}".encode()


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

IP = "192.168.111.40"
Split = "-||-"
Port = 24682
Buffer = 1024 * 64

Break = "Break"

Mode1 = "Mode1"
Mode2 = "Mode2"

AnalyticsMode = True

# Main part

Main.connect((IP, Port))
# camera = PiCamera()
#
# camera.resolution = (1280, 720)
# camera.vflip = True
# camera.contrast = 10

while True:
    Command = Read(Main, Buffer)
    if AnalyticsMode:
        # file_name = "/home/pi/Pictures/img_" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ".jpg"
        # camera.capture(file_name)
        # Img = plt.imread(file_name)
        Time = datetime.now()
        Img = ""
        Main.send(Parser(Data(Img, "", Time.year, Time.month, Time.day, Time.hour, Time.minute)))
    else:
        Main.send(Parser(Data("", "", 0, 0, 0, 0, 0)))
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
