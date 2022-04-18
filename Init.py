import json
from DataStore import InitDataset, GetTimely, YearlyReport, MonthlyReport, ClusteredMonthlyReport, DailyReport
from DataGenerator import Response, Header, Type, Report
import numpy as np
from Core import Init
import matplotlib.pyplot as plt
import requests
import cv2
import face_recognition
from DataStore import *
import os
import shutil
import requests


def telegram_notifications(msg):
    bot_token = '5347296207:AAHwOXopPpxUPkHElRhVSI_owg2R-xkXPfc'
    bot_chatID = '1190099465'
    send_text = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + bot_chatID + \
                "&parse_mode=MarkdownV2&text=" + msg + " is entering the shop." + " To monitor, follow the link" + \
                "http://youtube.com/channel/UCe9z1mihw-RBSV3RuXxO0lg/live"
    response = requests.get(send_text)
    return response.json()


IP = "0.0.0.0"
Df = InitDataset()
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
    global Df
    while True:
        Image = Read(Client, Buffer)
        Image = json.loads(Image)
        Img = np.array(Image["Image"])
        Client.send(Parser(CurrMode))

        Img = np.array(Img, dtype="uint8")
        cv2.imwrite("Tmp.jpeg", Img)
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
                known_face_encodings.append(encodeimg)

            criminaldata_path = "E:\\College\\Sem 6\\IoT\\Project\\Rasperry Pi Client\\Criminal"
            criminal_listing = os.listdir(criminaldata_path)
            criminal_face_encodings = []
            for file in criminal_listing:
                img = face_recognition.load_image_file(criminaldata_path + '\\' + file)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encodeimg = face_recognition.face_encodings(img)[0]
                criminal_face_encodings.append(encodeimg)

            known_face_names = [
                "Customer_1",
                "Customer_2",
                "Customer_3",
                "Customer_4",
            ]

            criminal_face_names = [
                "Criminal_1",
                "Criminal_2",
                "Criminal_3",
                "Criminal_4",
            ]

            i = 5
            matches = face_recognition.compare_faces(known_face_encodings, encodeimg_current)
            criminal_matches = face_recognition.compare_faces(criminal_face_encodings, encodeimg_current)
            name = "unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, encodeimg_current)
            criminal_face_distances = face_recognition.face_distance(criminal_face_encodings, encodeimg_current)
            best_match_index_1 = np.argmin(face_distances)
            best_match_index_2 = np.argmin(criminal_face_distances)
            if matches[best_match_index_1]:
                name = known_face_names[best_match_index_1]
                print(name)
                Out = AddEndTime(Df, name, Image["Year"], Image["Month"], Image["Date"], Image["Hour"], Image["Min"])
                if Out is None:
                    Df = AddRecord(Df, name, Image["Year"], Image["Month"], Image["Date"], Image["Hour"], Image["Min"],
                                   Image["Hour"], Image["Min"])
                else:
                    Df = Out
                Save(Df)
            else:
                print(known_face_names)
                cv2.imwrite(path + "\\" + "Customer_" + str(i) + ".jpg", Img)
                Df = AddRecord(Df, name, Image["Year"], Image["Month"], Image["Date"], Image["Hour"], Image["Min"],
                               Image["Hour"], Image["Min"])
                known_face_names.append("Customer_" + str(i))
                i += 1
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


Core = Init(IP)
Core.WebRequestProcessing = WebRequestProcessing
Core.TCPRequestProcessing = TCPPreprocessing
Core.TCPInputProcessing = ImageProcessing

Core.Start()
