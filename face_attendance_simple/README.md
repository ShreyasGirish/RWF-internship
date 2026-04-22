# Simple Face Recognition Attendance System

## Setup
1. Install dependencies:
```
pip install opencv-python face_recognition numpy
```
(Note: face_recognition may require cmake and Visual Studio Build Tools on Windows.)

2. Add face images to `Training_Images/` folder (filename = person's name, e.g. `John.jpg`).

## Run
```
python main.py
```

## Features
- Live webcam face recognition.
- Green box + name on match.
- Logs attendance to `Attendance.csv`.
- Press **Q** to quit.

## Output
Terminal shows encoding progress and attendance marks. OpenCV window for live video.
