import json
from DataGenerator import Response, Header, Type, Report
import numpy as np
from Core import Init
import matplotlib.pyplot as plt
import cv2
import face_recognition
from Queries import *
import os
import requests


def Clean(Msg: str):
    seq = [".", "-"]
    for i in seq:
        Msg = Msg.replace(i, "\\" + i)
    return Msg


def telegram_notifications(msg):
    bot_token = '5347296207:AAHwOXopPpxUPkHElRhVSI_owg2R-xkXPfc'
    bot_chatID = '1190099465'
    send_text = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + bot_chatID + \
                "&parse_mode=MarkdownV2&text=" + msg + " has entered the shop Please follow the link to monitor " + Clean(
        "http://youtube.com/channel/UCe9z1mihw-RBSV3RuXxO0lg/live")
    response = requests.get(send_text)
    return response.json()


IP = "0.0.0.0"
Split = "-||-"
Buffer = 1024 * 64


class Mode:
    Analytics = "Mode1"
    Intruder = "Mode2"


CurrMode = Mode.Analytics
Core = Init(IP)
InitTable(Core)


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
                       Report(GetByTimelyReport(Core), GetByDailyReport(Core), GetByWeeklyReport(Core),
                              GetByMonthlyReport(Core), GetByYearlyReport(Core),GetInsideCount(Core)))
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


known_face_names = [
    "CCHB101",
    "CCHB102",
    "CCHB103",
    "CCHB104",
]

criminal_face_names = [
    "Cid1",
    "Cid2",
]


def ImageProcessing(Client, Address):
    while True:
        Image = Read(Client, Buffer)
        Client.send(Parser(CurrMode))
        Image = json.loads(Image)
        if Image["Image"] == "":
            if Image["Command"] == "Detected":
                """
                Notification part here
                """
                pass
        else:
            Img = np.array(Image["Image"])
            Img = np.array(Img, dtype="uint8")
            Img = cv2.rotate(Img, cv2.ROTATE_180)
            plt.imshow(Img)
            plt.show()

            encodeimg_current = face_recognition.face_encodings(Img)
            if len(encodeimg_current) > 0:
                encodeimg_current = encodeimg_current[0]
                os.getlogin()
                path = 'E:\\College\\Sem 6\\IoT\\Project\\Rasperry Pi Client\\images'
                listing = os.listdir(path)
                known_face_encodings = []
                for file in listing:
                    img = face_recognition.load_image_file(path + '\\' + file)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    encodeimg = face_recognition.face_encodings(img)[0]
                    if len(encodeimg) > 0:
                        known_face_encodings.append(encodeimg)

                criminaldata_path = "E:\\College\\Sem 6\\IoT\\Project\\Rasperry Pi Client\\Criminal"
                criminal_listing = os.listdir(criminaldata_path)
                criminal_face_encodings = []
                for file in criminal_listing:
                    img = face_recognition.load_image_file(criminaldata_path + '\\' + file)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    encodeimg = face_recognition.face_encodings(img)[0]
                    if len(encodeimg) > 0:
                        criminal_face_encodings.append(encodeimg)

                i = 5
                matches = face_recognition.compare_faces(known_face_encodings, encodeimg_current)
                criminal_matches = face_recognition.compare_faces(criminal_face_encodings, encodeimg_current)
                face_distances = face_recognition.face_distance(known_face_encodings, encodeimg_current)
                criminal_face_distances = face_recognition.face_distance(criminal_face_encodings, encodeimg_current)
                best_match_index_1 = np.argmin(face_distances)
                best_match_index_2 = np.argmin(criminal_face_distances)
                if matches[best_match_index_1]:
                    name = known_face_names[best_match_index_1]
                    print(name)
                else:
                    cv2.imwrite(path + "\\" + "C" + str(i) + ".jpg", Img)
                    known_face_names.append("Customer_" + str(i))
                    i += 1
                Nam = int(best_match_index_1 + 1)
                if Image["CameraID"] == 2:
                    ExitStamp(Core, Nam)
                elif Image["CameraID"] == 1:
                    EntryStamp(Core, Nam)
                if criminal_matches[best_match_index_2]:
                    criminal_name = criminal_face_names[best_match_index_2]
                    print("Criminal entering")
                    telegram_notifications(criminal_name)

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
