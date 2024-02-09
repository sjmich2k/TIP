
import numpy as np


def parse_swipes(window):
    """
    Determine which axis has the most variance of optical flow over a window.

    @param window:  a queue of [ average horizontal flow, average vertical flow ]
    @return:        swipe direction with its strength
    """

    n = window.qsize()

    # Split 2D vector field into scalar lists
    motion_pos_x = np.zeros(n)
    motion_neg_x = np.zeros(n)
    motion_pos_y = np.zeros(n)
    motion_neg_y = np.zeros(n)

    for i in range(n):
        motion_x = window.queue[i][0]
        if motion_x > 0:
            motion_pos_x[i] = abs(motion_x)
        if motion_x < 0:
            motion_neg_x[i] = abs(motion_x)

        motion_y = window.queue[i][1]
        if motion_y > 0:
            motion_pos_y[i] = abs(motion_y)
        if motion_y < 0:
            motion_neg_y[i] = abs(motion_y)

    # Calculate variances
    motion_var_px = 2 * np.var(motion_pos_x)
    motion_var_nx = 2 * np.var(motion_neg_x)
    motion_var_py = 2 * np.var(motion_pos_y)
    motion_var_ny = 2 * np.var(motion_neg_y)

    # [ right, left, up, down ]
    dir_strength = np.array([
        motion_var_px,
        motion_var_nx,
        motion_var_py,
        motion_var_ny
    ])
    max_index = np.argmax(dir_strength)

    # Return the direction with the greatest variation
    if abs(dir_strength[max_index]) > 0.1:
        if max_index == 0:
            return ["RIGHT", dir_strength[max_index]]
        if max_index == 1:
            return ["LEFT", dir_strength[max_index]]
        if max_index == 2:
            return ["UP", dir_strength[max_index]]
        if max_index == 3:
            return ["DOWN", dir_strength[max_index]]

    return ["NONE", 0]
