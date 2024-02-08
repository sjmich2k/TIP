
import numpy as np


def parse_zoom(window, filter_x, filter_y):

    n = window.qsize()
    dot_products = []

    for i in range(0, n):
        frame = window.queue[i]
        frame_x = frame[:, :, 0]
        frame_y = frame[:, :, 1]
        dot = frame_x * filter_x + frame_y * filter_y
        dot_products.append(np.mean(dot))

    strength = np.mean(np.array(dot_products)) / 80
    if strength > 0:
        return ["ZOUT", abs(strength)]
    return ["ZIN", abs(strength)]


def create_zoom_filter(width, height):

    # Calculate the center point of the screen
    center_x = width // 2
    center_y = height // 2

    # Create an empty image with the same shape as the flow field
    opposite_vec_x = np.zeros((height, width))
    opposite_vec_y = np.zeros((height, width))

    # Fill the image with vectors pointing to the opposite direction from the center
    for y in range(height):
        for x in range(width):
            opposite_vec_x[y, x] = center_x - x
            opposite_vec_y[y, x] = center_y - y

    return opposite_vec_x, opposite_vec_y
