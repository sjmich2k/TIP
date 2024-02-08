
import numpy as np


def parse_swipes(window):
    """

    @param window:  a python queue containing
    @return:
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
    motion_var_px = np.var(motion_pos_x)
    motion_var_nx = np.var(motion_neg_x)
    motion_var_py = np.var(motion_pos_y)
    motion_var_ny = np.var(motion_neg_y)

    p_px = np.histogram(motion_pos_x, bins=256, range=(0, 255))[0] / float(len(motion_pos_x))
    p_nx = np.histogram(motion_neg_x, bins=256, range=(0, 255))[0] / float(len(motion_neg_x))
    p_py = np.histogram(motion_pos_y, bins=256, range=(0, 255))[0] / float(len(motion_pos_y))
    p_ny = np.histogram(motion_neg_y, bins=256, range=(0, 255))[0] / float(len(motion_neg_y))

    entropy_px = -np.sum(p_px * np.log2(p_px + 1e-6))
    entropy_nx = -np.sum(p_nx * np.log2(p_nx + 1e-6))
    entropy_py = -np.sum(p_py * np.log2(p_py + 1e-6))
    entropy_ny = -np.sum(p_ny * np.log2(p_ny + 1e-6))

    # [ right, left, up, down ]
    ego_motion = np.array([
        (motion_var_px + entropy_px) / 2,
        (motion_var_nx + entropy_nx) / 2,
        (motion_var_py + entropy_py) / 2,
        (motion_var_ny + entropy_ny) / 2
    ])
    # ego_motion = np.array([px, nx, py, ny, psy, pny])
    max_index = np.argmax(ego_motion)

    if abs(ego_motion[max_index]) > 0.1:
        if max_index == 0:
            return ["RIGHT", ego_motion[max_index]]
        if max_index == 1:
            return ["LEFT", ego_motion[max_index]]
        if max_index == 2:
            return ["UP", ego_motion[max_index]]
        if max_index == 3:
            return ["DOWN", ego_motion[max_index]]
        # if max_index == 4:
        #     return "scroll up - " + str(ego_motion[max_index])
        # if max_index == 5:
        #     return "scroll down - " + str(ego_motion[max_index])

    return ["NONE", 0]
