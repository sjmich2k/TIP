
import cv2
import numpy as np

def parse_typing(diff, width, height):
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    xx = []
    yy = []
    for contour in contours:
        # Calculate the center of the contour
        moments = cv2.moments(contour)
        if moments['m00'] != 0:
            xx.append(int(moments['m10'] / moments['m00']))
            yy.append(int(moments['m01'] / moments['m00']))

    if len(xx) == 0:
        return "NONE"

    pos = (np.mean(xx), np.mean(yy))
    if pos[0] < width / 2 and pos[1] > height / 2:
        return "TYPEL"
    if pos[0] > width / 2 and pos[1] > height / 2:
        return "TYPER"

    return "NONE"
