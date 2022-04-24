from socket import *
import json
from picamera import PiCamera
from datetime import datetime
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)


def Data(Image, Command, Year, Month, Date, Hour, Min):
    Out = {
        "CameraID": 2,
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
StopStream = "Stop"
Mode1 = "Mode1"
Mode2 = "Mode2"

AnalyticsMode = True

# Main part
while True:
    try:
        Main.connect((IP, Port))
        break
    except Exception:
        pass

camera = PiCamera()

camera.resolution = (200, 200)
camera.vflip = True
camera.contrast = 10


def Parser(String):
    return f"{len(String)}{Split}{String}".encode()


while True:
    file_name = "/home/pi/Pictures/img_tmp" + ".jpg"
    camera.capture(file_name)
    Img = plt.imread(file_name)
    Time = datetime.now()
    Main.send(Parser(Data(Img.tolist(), "", Time.year, Time.month, Time.day, Time.hour, Time.minute)))
    Command = Read(Main, Buffer)
    print(Command)
    if Command == Mode1:
        AnalyticsMode = True
    elif Command == Mode2:
        AnalyticsMode = False
    elif Command == Break:
        break
    elif Command == StopStream:
        pass
    else:
        pass

Main.close()
