import requests
import os
import keyboard
import cv2
import time

url = 'http://localhost:8000/api/proj/'  

unique_string = 'door21'

def record_webcam_video():
    cap = cv2.VideoCapture(0)
    file_name = 'webcam_video.mp4'
    file_path = os.path.join(os.getcwd(), file_name)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(file_path, fourcc, 20.0, (640, 480))

    start_time = time.time()
    frame_count = 0  

    while time.time() - start_time < 8:
        ret, frame = cap.read()
        if ret:
            frame_count += 1

            if time.time() - start_time >= 4:
                out.write(frame)

            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return file_path

def send_post_request(file_path):
    with open(file_path, 'rb') as file:
        files = {'video': (file.name, file, 'video/mp4')}
        data = {'unique_string': unique_string}
        response = requests.post(url, data=data, files=files)

    print(response.status_code)
    print(response.json())

print("Press 'a' to record a webcam video and send the POST request, or 'q' to quit.")
while True:
    if keyboard.is_pressed('a'):
        video_path = record_webcam_video()
        # video_path = 'videoRyan3.mp4'
        send_post_request(video_path)
    elif keyboard.is_pressed('q'):
        break
