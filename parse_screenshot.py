import numpy as np


def parse_screenshot(arr, threshold, percentage):
    total_elements = arr.size
    count_above_threshold = np.sum(arr > threshold)
    percent_above_threshold = count_above_threshold / total_elements

    if percent_above_threshold > percentage:
        return True
    else:
        return False

