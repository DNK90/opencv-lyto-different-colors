import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui
from time import sleep


def find_different(arr):
    for num, i in enumerate(arr):
        if arr.count(i) == 1:
            return num
    else:
        return 0

originalX = 480
originalY = 600
top = 300
left = 800

currentR = 0

mon = {'top': top, 'left': left, 'width': originalX, 'height': originalY}

sct = mss()
print(pyautogui.size()[0])
start = False
counter = 0
while counter < 100000000000:
    sct.get_pixels(mon)
    img = np.array(Image.frombytes('RGB', (sct.width, sct.height), sct.image))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 10)
    if start:
        try:
            counter += 1
            if circles is not None:
                # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")
                # loop over the (x, y) coordinates and radius of the circles
                this = []
                for (x, y, r) in circles:
                    this.append(list(img[y, x, :]))
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                nn = find_different(this)
                for num, (x, y, r) in enumerate(circles):
                    if num == nn:
                        point = pyautogui.position()
                        pyautogui.click(top+x/2, left+y/2, 1)

                        cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                        cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        except Exception as e:
            print(e)

    cv2.imshow('test', np.array(img))

    if cv2.waitKey(1) & 0xFF == ord('s'):
        start = start is False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    sleep(0.06)