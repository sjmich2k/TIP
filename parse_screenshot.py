import numpy as np


def parse_screenshot(arr, threshold, percentage):
    """
    Check if certain percentage of pixels are greater than a threshold to detect screenshots.

    :param arr:         2D field (frame) of grayscale pixel intensities
    :param threshold:   intensity threshold (max. 255)
    :param percentage:  percentage of pixels > threshold to detect screenshot
    :return:            boolean indicating screenshot likeliness
    """

    total_elements = arr.size
    count_above_threshold = np.sum(arr > threshold)
    percent_above_threshold = count_above_threshold / total_elements

    if percent_above_threshold > percentage:
        return True
    else:
        return False

