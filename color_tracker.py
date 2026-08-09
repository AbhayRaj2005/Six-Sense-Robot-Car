"""
Sixth Sense Bot - Color Tracking Controller
--------------------------------------------
Tracks a chosen color object via webcam and sends movement commands
('F','B','L','R','S') to the Arduino over Serial to drive the bot.

Requires: opencv-python, imutils, numpy, pyserial
Install:  pip install -r requirements.txt
"""

import time

import cv2
import imutils
import numpy as np
import serial

# ----- Serial Configuration -----
SERIAL_PORT = "COM3"      # Change this to your Arduino's port
                           # Windows: "COM3", "COM4", ...
                           # Mac/Linux: "/dev/ttyUSB0" or "/dev/ttyACM0"
BAUD_RATE = 9600

# ----- Color Ranges (HSV) -----
COLOR_BUCKET_HSV = {
    "black": [[180, 255, 30], [0, 0, 0]],
    "white": [[180, 30, 255], [0, 0, 200]],
    "red": [[10, 255, 255], [0, 100, 100]],
    "green": [[80, 255, 255], [40, 40, 40]],
    "blue": [[130, 255, 255], [90, 50, 50]],
    "yellow": [[30, 255, 255], [20, 100, 100]],
    "purple": [[160, 255, 255], [120, 50, 50]],
    "orange": [[30, 255, 255], [0, 100, 100]],
    "gray": [[180, 30, 150], [0, 0, 0]],
}

COLOR_OPTIONS = {
    "1": "black", "2": "white", "3": "red", "4": "green", "5": "blue",
    "6": "yellow", "7": "purple", "8": "orange", "9": "gray", "10": "custom",
}

# ----- Tracking Zones (matched to a 320x330 ROI starting at x=300, y=10) -----
UP_RECT = ((410, 10), (520, 120))
DOWN_RECT = ((410, 230), (520, 340))
MID_RECT = ((410, 120), (520, 230))
LEFT_RECT = ((300, 120), (410, 230))
RIGHT_RECT = ((520, 120), (630, 230))

# ----- Command map: zone -> Arduino Serial command -----
COMMAND_MAP = {
    "u": b"F",   # forward
    "d": b"B",   # backward
    "l": b"L",   # left
    "r": b"R",   # right
    "m": b"S",   # stop / middle
}


def input2range(data: str) -> np.array:
    data = data.split(",")
    return np.array([int(x.strip()) for x in data])


def point_in_rectangle(rect, pt):
    x1, y1 = rect[0]
    x2, y2 = rect[1]
    p1, p2 = pt
    if p1 is None or p2 is None:
        return False
    return x1 < p1 < x2 and y1 < p2 < y2


def draw_rectangles(img: np.array, active_rect: str = None) -> np.array:
    img = cv2.rectangle(img, UP_RECT[0], UP_RECT[1], (255, 0, 0), 3)
    img = cv2.rectangle(img, DOWN_RECT[0], DOWN_RECT[1], (255, 0, 0), 3)
    img = cv2.rectangle(img, MID_RECT[0], MID_RECT[1], (255, 0, 0), 3)
    img = cv2.rectangle(img, LEFT_RECT[0], LEFT_RECT[1], (255, 0, 0), 3)
    img = cv2.rectangle(img, RIGHT_RECT[0], RIGHT_RECT[1], (255, 0, 0), 3)

    zone_rects = {"u": UP_RECT, "d": DOWN_RECT, "m": MID_RECT, "l": LEFT_RECT, "r": RIGHT_RECT}
    if active_rect in zone_rects:
        r = zone_rects[active_rect]
        img = cv2.rectangle(img, r[0], r[1], (0, 255, 0), 3)
    return img


def connect_serial(port: str, baud: int):
    try:
        ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2)  # allow Arduino to reset after connection opens
        print(f">> Connected to Arduino on {port}")
        return ser
    except serial.SerialException as err:
        print(f"!! Could not open serial port {port}: {err}")
        print("!! Check SERIAL_PORT at the top of this script and try again.")
        return None


def main():
    print("*" * 80)
    print("Sixth Sense Bot - Color Tracking Controller")
    print("*" * 80)

    ser = connect_serial(SERIAL_PORT, BAUD_RATE)

    print("\n!! Make sure the tracked object is round / a solid single color !!\n")

    obj_color = None
    while obj_color is None:
        print("Choose object color")
        for k, v in COLOR_OPTIONS.items():
            print(k, " -- ", v)
        choice = input(">> ")
        obj_color = COLOR_OPTIONS.get(choice, None)

    print(f">> {obj_color} selected")

    if obj_color != "custom":
        higher_range = np.array(COLOR_BUCKET_HSV[obj_color][0])
        lower_range = np.array(COLOR_BUCKET_HSV[obj_color][1])
    else:
        higher_range = input2range(input(">> Higher range (comma separated H,S,V): "))
        lower_range = input2range(input(">> Lower range (comma separated H,S,V): "))

    print("Higher range: ", higher_range)
    print("Lower range: ", lower_range)

    last_status = "s"
    cam = cv2.VideoCapture(0)

    try:
        while True:
            check, frame = cam.read()
            if not check:
                print("Could not read from camera")
                break

            frame = cv2.flip(frame, 1)
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv_frame[10:340, 300:630], lower_range, higher_range)
            cv2.imshow("mask", mask)

            contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            status = "m"
            active_rect = None
            cx, cy = None, None

            if contours:
                largest = max(contours, key=cv2.contourArea)
                moments = cv2.moments(largest)
                if moments["m00"] != 0.0:
                    cx = int(moments["m10"] / moments["m00"]) + 300
                    cy = int(moments["m01"] / moments["m00"]) + 10
                    cv2.circle(frame, (cx, cy), 3, (255, 255, 255), 3)

            if point_in_rectangle(UP_RECT, (cx, cy)):
                status, active_rect = "u", "u"
            elif point_in_rectangle(DOWN_RECT, (cx, cy)):
                status, active_rect = "d", "d"
            elif point_in_rectangle(MID_RECT, (cx, cy)):
                status, active_rect = "m", "m"
            elif point_in_rectangle(LEFT_RECT, (cx, cy)):
                status, active_rect = "l", "l"
            elif point_in_rectangle(RIGHT_RECT, (cx, cy)):
                status, active_rect = "r", "r"

            frame = draw_rectangles(frame, active_rect)
            cv2.imshow("processed frame", frame)

            if status != last_status:
                last_status = status
                command = COMMAND_MAP.get(status, b"S")
                if ser is not None:
                    ser.write(command)
                print(f">> Sent command: {command}")

            key = cv2.waitKey(33)
            if key == 27:  # ESC to quit
                break
    finally:
        if ser is not None:
            ser.write(b"S")  # stop the bot on exit
            ser.close()
        cv2.destroyAllWindows()
        cam.release()


if __name__ == "__main__":
    main()
