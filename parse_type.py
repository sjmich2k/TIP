
import cv2
import numpy as np


def parse_typing(diff, width, height):
    """
    Find areas of differences and check if they are happening at the bottom left/right of the screen.

    :param diff:    2D field of pixel differences
    :param width:   width of the screen
    :param height:  height of the screen
    :return:        none / left type / right type
    """

    # Find areas where there are pixel differences
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Collect contour centroids into lists
    xx = []
    yy = []
    for contour in contours:
        moments = cv2.moments(contour)
        if moments['m00'] != 0:
            xx.append(int(moments['m10'] / moments['m00']))
            yy.append(int(moments['m01'] / moments['m00']))

    if len(xx) == 0:
        return "NONE"

    # Determine if the centroid of the centroids are at the screen's bottom left or right
    pos = (np.mean(xx), np.mean(yy))
    if pos[0] < width / 2 and pos[1] > height / 2:
        return "TYPEL"
    if pos[0] > width / 2 and pos[1] > height / 2:
        return "TYPER"

    return "NONE"
