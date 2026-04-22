import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# --- CONFIGURATION ---
PATH = 'Training_Images'
ATTENDANCE_FILE = 'Attendance.csv'
SCALE_FACTOR = 0.25  # Resize frame to 1/4 for faster processing
TOLERANCE = 0.6      # Lower is stricter, higher is more loose

print("Face Recognition Attendance System")
print("Make sure to add face images to 'Training_Images' folder (filename = name.jpg)")

images = []
classNames = []
try:
    myList = os.listdir(PATH)
    print(f'Found {len(myList)} images in training folder.')

    # Load images and extract names
    for cl in myList:
        curImg = cv2.imread(f'{PATH}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        print(f'Loaded: {os.path.splitext(cl)[0]}')
except FileNotFoundError:
    print(f"No 'Training_Images' folder found. Creating empty encodings.")
    encodeListKnown = []

if images:
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    print('Encoding Started... Please wait.')
    encodeListKnown = findEncodings(images)
    print('Encoding Complete.')
else:
    encodeListKnown = []

def markAttendance(name):
    with open(ATTENDANCE_FILE, 'a') as f:  # Use 'a' to append
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        f.write(f'\n{name},{dtString}')
        print(f"✅ Attendance Marked for: {name}")

# Start Webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    # Resize for performance and convert to RGB
    imgSmall = cv2.resize(img, (0, 0), None, SCALE_FACTOR, SCALE_FACTOR)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    # Detect faces in current frame
    facesCurFrame = face_recognition.face_locations(imgSmall)
    encodesCurFrame = face_recognition.face_encodings(imgSmall, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        
        if faceDis.size > 0:
            matchIndex = np.argmin(faceDis)
            
            if matches[matchIndex] and faceDis[matchIndex] < TOLERANCE:
                name = classNames[matchIndex].upper()
                
                # Rescale coordinates to original frame size
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1/0.25, x2/0.25, y2/0.25, x1/0.25
                
                # Draw UI box and name
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                
                markAttendance(name)

    cv2.imshow('Face Attendance - Press Q to Quit', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Attendance session ended.")
