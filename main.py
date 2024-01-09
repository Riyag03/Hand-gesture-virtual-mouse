from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import pyautogui as pyt

app = Flask(__name__)

cam = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
ind_y = 0
screen_width, screen_height = pyt.size()
smooth = 20
px, py = 0, 0
cx, cy = 0, 0


def gen():
    global ind_y, px, py, cx, cy
    
    while True:
        check, frame = cam.read()
        frame = cv2.flip(frame, 1)

        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks

        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark

                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)

                    if id == 8:
                        cv2.circle(img=frame, center=(x, y), radius=15, color=(0, 255, 255))
                        ind_x = (screen_width / frame_width) * x
                        ind_y = (screen_height / frame_height) * y

                        cx = px + (ind_x - px) / smooth
                        cy = py + (ind_y - py) / smooth
                        pyt.moveTo(cx, cy)
                        px, py = cx, cy

                    if id == 4:
                        cv2.circle(img=frame, center=(x, y), radius=15, color=(0, 255, 255))
                        thumb_x = (screen_width / frame_width) * x
                        thumb_y = (screen_height / frame_height) * y
                        print('distance : ', abs(ind_y - thumb_y))
                        if abs(ind_y - thumb_y) < 70:
                            print('click')
                            pyt.click()
                            pyt.sleep(5)

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


