import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui
from time import sleep


LIMIT_CLICKED = 50
MAX_R = 130
SLEEP = 0.06


def find_different(arr):
    # there is only one unique case, if the second happens then quit and wait for next time.
    counter = 0
    n = 0
    for num, i in enumerate(arr):
        if arr.count(i) == 1:
            n = num
            counter += 1
        if counter > 1:
            print("found duplicated circles")
            return 0
    return n


if __name__ == "__main__":

    width = 480
    height = 600
    top = 400
    left = 800
    clicked = dict()

    mon = {'top': top, 'left': left, 'width': width, 'height': height}

    sct = mss()
    start = False

    while 1:
        sct.get_pixels(mon)
        img = np.array(Image.frombytes('RGB', (sct.width, sct.height), sct.image))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if start:
            try:
                circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 10)
                if circles is not None:
                    # convert the (x, y) coordinates and radius of the circles to integers
                    circles = np.round(circles[0, :]).astype("int")
                    # loop over the (x, y) coordinates and radius of the circles
                    this = []

                    for (x, y, r) in circles:
                        # only find_different with circles that is in allowed R
                        if r < MAX_R:
                            this.append(list(img[y, x, :]))

                    nn = find_different(this)
                    if nn > 0:
                        for num, (x, y, r) in enumerate(circles):
                            if num == nn:
                                # calculate to real position and trigger click event
                                posX = left + (x / 2)
                                posY = top + (y / 2)
                                key = "{}-{}".format(posX, posY)
                                pyautogui.click(posX, posY, 1)

                                if key not in clicked:
                                    clicked[key] = 1
                                elif clicked[key] > LIMIT_CLICKED:
                                    clicked = dict()
                                    start = False
                                else:
                                    clicked[key] += 1
                                print("position:{} has been clicked:{} (times)".format(key, clicked[key]))

                                # draw the circle in the output image, then draw a rectangle
                                # corresponding to the center of the circle
                                cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                                cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

                                # wait for new frame loading, reduce the capability of wrong detection
                                sleep(SLEEP)

            except Exception as e:
                print(e)

        cv2.imshow('test', np.array(img))

        if cv2.waitKey(1) & 0xFF == ord('s'):
            start = start is False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
