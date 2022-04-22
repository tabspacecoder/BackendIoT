import cv2
import face_recognition
import numpy as np
import os
import shutil
import requests


def telegram_notifications(msg):
    bot_token = '5347296207:AAHwOXopPpxUPkHElRhVSI_owg2R-xkXPfc'
    bot_chatID = '1190099465'
    headers_ = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    send_text = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + bot_chatID + "&parse_mode=MarkdownV2&text=" + "ALERT!!" + msg + " is entering the shop"
    response = requests.get(send_text)
    # response = requests.get(f"https://api.telegram.org/bot5347296207:AAHwOXopPpxUPkHElRhVSI_owg2R-xkXPfc
    # /sendMessage?chat_id=?{bot_chatID}&parse_mode=MarkdownV2&text=ALERT!!?{msg}is entering the shop",
    # headers=headers_)
    print(response)
    print(response.json)
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
        telegram_notifications(criminal_name)
face_names.append(name)
print(name)
print(criminal_name)
