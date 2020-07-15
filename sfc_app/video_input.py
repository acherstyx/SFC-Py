import cv2

cap = cv2.VideoCapture("video_sample.mp4")

while cap.isOpened():
    ret, fram = cap.read()
    cv2.imshow("image", fram)
