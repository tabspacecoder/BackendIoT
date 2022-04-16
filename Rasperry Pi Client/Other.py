import cv2
import face_recognition
import numpy as np
import os
import shutil

# 2 images compare
os.getlogin()
path = 'C:\\Users\\nikhi\\Downloads\\images'
listing = os.listdir(path)
known_face_encodings = []
for file in listing:
    img = face_recognition.load_image_file(path+'\\'+file)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    encodeimg = face_recognition.face_encodings(img)[0]
    known_face_encodings.append(encodeimg)

#faceLoc = face_recognition.face_locations(imgelon)[0] #returns 4 vals
#face_landmarks_list = face_recognition.face_landmarks(imgelon) #facial features

#print(faceLoc)
#print(face_landmarks_list)

#cv2.rectangle(imgelon,() )

#results = face_recognition.compare_faces([encodeElon], encodejane)

#if results[0] == True:
#   print("Match!")
#else:
#    print("Mis-Match!")

#cv2.imshow('Elon Musk',imgelon)
#cv2.imshow('Jane Doe',imgjane)
#cv2.waitKey(0)

###########


known_face_names = [
    "Customer_1",
    "Customer_2",
    "Customer_3",
    "Customer_4",
]
i = 5
face_encodings = []
current_path = 'C:\\Users\\nikhi\\Downloads\\currentimg'
current_listing = os.listdir(current_path)

while 1:
    face_encodings = []
    for f in current_listing:
        frame = face_recognition.load_image_file(current_path+'\\'+f)
        img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        encodeimg = face_recognition.face_encodings(img)[0]
        face_encodings.append(encodeimg)
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        else:
            shutil.copy(face_encoding,path)
            os.rename(face_encoding, "Customer_"+i)
            i+=1
        print(name)
        face_names.append(name)