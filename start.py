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


if __name__ == "__main__":

    width = 480
    height = 600
    top = 300
    left = 800

    mon = {'top': top, 'left': left, 'width': width, 'height': height}

    sct = mss()
    start = False
    counter = 0

    # set a counter to 2000 (0.06*2000=120s) to prevent infinite loop in case user cannot exit from a mess of clicking...lol
    while counter < 2000:
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
                            pyautogui.click(left + (x / 2), top + (y / 2), 1)

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
