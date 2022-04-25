import cv2
import face_recognition
import numpy as np
import os
import shutil
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


# main
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
    "CCHB101",
    "CCHB102",
    "CCHB103",
    "CCHB104",
]

criminal_face_names = [
    "Cid1",
    "Cid2",
]

i = 5

current_path = 'E:\\College\\Sem 6\\IoT\\Project\\Rasperry Pi Client\\currentimg'
current_listing = os.listdir(current_path)

face_encodings = []
for f in current_listing:
    frame = face_recognition.load_image_file(current_path + '\\' + f)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    print(img.shape)
    encodeimg = face_recognition.face_encodings(img)[0]
    face_encodings.append(encodeimg)
face_names = []
for face_encoding in face_encodings:
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    criminal_matches = face_recognition.compare_faces(criminal_face_encodings, face_encoding)
    name = "unknown"
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    criminal_face_distances = face_recognition.face_distance(criminal_face_encodings, face_encoding)
    best_match_index_1 = np.argmin(face_distances)
    best_match_index_2 = np.argmin(criminal_face_distances)
    if matches[best_match_index_1]:
        name = known_face_names[best_match_index_1]
    else:
        shutil.copy(face_encoding, path)
        os.rename(face_encoding, "Customer_" + i)
        i += 1
    if criminal_matches[best_match_index_2]:
        criminal_name = criminal_face_names[best_match_index_2]
        print("Criminal entering")
        print(telegram_notifications(criminal_name))
    print(name)
    print(criminal_name)
