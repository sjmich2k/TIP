
import cv2
import numpy as np
import queue
import serial
import sys
import tkinter as tk
from tkinter.filedialog import askopenfilename

from parse_swipes import parse_swipes
from parse_type import parse_typing
from parse_zoom import parse_zoom, create_zoom_filter
from parse_screenshot import parse_screenshot
from play_sound import play_sound, no_sound, end

# IO
VIDEO_FILE = None
ser_swipe_lr = None
ser_swipe_ud = None
ser_type = None
ser_screenshot = None
ser_scroll = None
ser_zoom = None


# --------------------------
# CONFIGURATION

WIDTH = 150                 # resize width (px)
HEIGHT = 325                # resize height (px)
SKIP_TO = 0                 # start from (sec)

DELTA_TIME = 0.6            # clock speed (sec)
MOTION_COOLDOWN = 1         # cooldown after swipes / zooms (sec)
SCREENSHOT_COOLDOWN = 2     # cooldown after screenshots (sec)

SWIPE_THRESHOLD = 0.45      # swipe calibration
ZOOM_THRESHOLD = 0.68       # zoom calibration
SCREENSHOT_THRESHOLD = 200  # screenshot calibration (max. 255)

SHOW_IMG = True             # show real-time debug video
SHOW_SHEET = True           # show real-time sheet output
WRITE_TO_SERIAL = False     # output to usb-connected devices

if WRITE_TO_SERIAL:
    ser_swipe_ud =      serial.Serial('SWIPE UP & DOWN device',     9600)
    ser_type =          serial.Serial('TYPE device',                9600)
    ser_screenshot =    serial.Serial('SCREENSHOT device',          9600)
    ser_scroll =        serial.Serial('SCROLL device',              9600)
    ser_swipe_lr =      serial.Serial('SWIPE LEFT & RIGHT device',  9600)
    ser_zoom =          serial.Serial('ZOOM device',                9600)

# CONFIGURATION
# --------------------------


# PROMPT TO SELECT VIDEO FILE (MAC)
if sys.platform == 'darwin':
    try:
        from AppKit import NSOpenPanel
    except ImportError:
        print("System is not macOS")
        sys.exit(1)
    open_panel = NSOpenPanel.openPanel()
    open_panel.setCanChooseFiles_(True)
    open_panel.setCanChooseDirectories_(False)
    if open_panel.runModal() == 1:
        VIDEO_FILE = open_panel.URL().path()

# PROMPT TO SELECT VIDEO FILE (WINDOWS)
if sys.platform == 'win32':
    root = tk.Tk()
    root.withdraw()
    VIDEO_FILE = askopenfilename(title="Select Screen Recording")

if VIDEO_FILE is None:
    print("No Screen Recording Selected")
    exit(1)


# SETUP VIDEO PARAMETERS
cap = cv2.VideoCapture(VIDEO_FILE)
raw_fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_FRAMES, SKIP_TO * raw_fps)
delta_frame = int(round(raw_fps * DELTA_TIME))
print("Video is {} fps, parsing every {} frames".format(raw_fps, delta_frame))


# CREATE WINDOW (25% of fps)
win_size = int(round(raw_fps / 4))
print('Window size: {}'.format(win_size))
swipe = queue.Queue(maxsize=win_size)
zoom = queue.Queue(maxsize=win_size)

# DEFINE SERIAL OUTPUTS & FREQUENCY ARRAY
motion_types = ["R", "L", "U", "D", "+", "-"]
motion_freq = np.array([0, 0, 0, 0, 0, 0])
# SCROLL UP: W, SCROLL DOWN: S
# Type Left: N, Type Right: M, B: Both
type_types = ['N', 'M', 'B']
type_freq = np.array([0, 0])

# TRACKING VARIABLES
screenshot = False
last_type = False
last_swipe = ''
cooldown = 0
sound_played = False

# CREATE VECTOR FIELD FOR PARSING ZOOM
zoom_filter_x, zoom_filter_y = create_zoom_filter(WIDTH, HEIGHT)

# INITIALIZE VIDEO FRAME ITERATION
success, frame_full = cap.read()
frame = cv2.resize(frame_full, (WIDTH, HEIGHT))
count = 0

# INITIALIZE DEBUG VIDEO WINDOW
if SHOW_IMG:
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', WIDTH * 2, HEIGHT * 2)

# MAIN VIDEO ITERATION
while success:

    # --- READ FRAME
    last_frame = frame
    success, frame_full = cap.read()
    frame = cv2.resize(frame_full, (WIDTH, HEIGHT))

    # --- PRE-PROCESS FRAMES
    last_gray = cv2.cvtColor(last_frame, cv2.COLOR_BGR2GRAY)
    last_blur = cv2.GaussianBlur(last_gray, (7, 7), 0)
    curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    curr_blur = cv2.GaussianBlur(curr_gray, (7, 7), 0)

    # --- SCREENSHOT
    if not screenshot:
        screenshot = parse_screenshot(curr_gray, SCREENSHOT_THRESHOLD, 0.95)

    # --- OPTICAL FLOW
    flow_params = dict(pyr_scale=0.5, levels=3, winsize=15, iterations=3, poly_n=5, poly_sigma=1.1, flags=0)
    flow = cv2.calcOpticalFlowFarneback(last_blur, curr_blur, None, **flow_params)

    # --- PIXEL DIFFERENCE (TYPING)
    diff = cv2.absdiff(last_gray, curr_gray)
    typing = parse_typing(diff, WIDTH, HEIGHT)

    # --- ZOOM
    if zoom.qsize() >= win_size:
        zoom.get()
    zoom.put(flow)
    zoom_strength = ["NONE", 0]
    if zoom.qsize() >= win_size:
        zoom_strength = parse_zoom(zoom, zoom_filter_x, zoom_filter_y)

    # --- SWIPES
    if swipe.qsize() >= win_size:
        swipe.get()
    swipe.put(np.mean(flow, axis=(0, 1)))
    swipe_strength = ["NONE", 0]
    if swipe.qsize() >= win_size:
        swipe_strength = parse_swipes(swipe)

    # --- DECIDE MOTION (SWIPE & ZOOM) FOR WINDOW, FREQUENCY++
    if zoom_strength[1] >= ZOOM_THRESHOLD:
        if zoom_strength[0] == "ZIN":
            motion_freq[4] += 3
        if zoom_strength[0] == "ZOUT":
            motion_freq[5] += 3
    if zoom_strength[1] < ZOOM_THRESHOLD:
        # no zooms, check motion
        if swipe_strength[1] > SWIPE_THRESHOLD:
            if swipe_strength[0] == "RIGHT":
                motion_freq[0] += 3
            if swipe_strength[0] == "LEFT":
                motion_freq[1] += 3
            if swipe_strength[0] == "UP":
                motion_freq[2] += 3
            if swipe_strength[0] == "DOWN":
                motion_freq[3] += 3
        # no motion, check for types
        if swipe_strength[1] < 0.0001:
            if typing == "TYPER":
                type_freq[0] += 1
            if typing == "TYPEL":
                type_freq[1] += 1

    # --- DEBUG VIDEO - show next frame
    delay = int(1000 / raw_fps)
    if SHOW_IMG:
        cv2.imshow('image', frame_full)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    # --- CLOCK - PRODUCE OUTPUT
    if count % delta_frame == 0:
        sound_played = False

        # check if output is in cooldown
        if cooldown > 0:
            cooldown -= DELTA_TIME

        else:
            if screenshot:
                print('SCREENSHOT')
                sound_played = play_sound('SCREENSHOT')
                if ser_screenshot is not None:
                    ser_screenshot.write('O'.encode(encoding="utf-8"))
                screenshot = False
                cooldown = SCREENSHOT_COOLDOWN

            else:
                # no screenshots, check for motion (swipe & zoom)
                arg_max = np.argmax(motion_freq)

                # frequency is over 1/4 of the window size
                if motion_freq[arg_max] > int(delta_frame / 4):

                    # last output was also 'UP' - SCROLL UP
                    if arg_max == 2 and last_swipe == 'UP':
                        print('SCROLL UP')
                        sound_played = play_sound('W')
                        if ser_scroll is not None:
                            ser_scroll.write('W'.encode(encoding="utf-8"))
                        last_swipe = 'UP'

                    # last output was also 'DOWN' - SCROLL DOWN
                    if arg_max == 3 and last_swipe == 'DOWN':
                        print('SCROLL DOWN')
                        sound_played = play_sound('S')
                        if ser_scroll is not None:
                            ser_scroll.write('S'.encode(encoding="utf-8"))
                        last_swipe = 'DOWN'

                    # different motion output from last output
                    if not (arg_max == 2 and last_swipe == 'UP') and not (arg_max == 3 and last_swipe == 'DOWN'):
                        print(motion_types[arg_max])
                        sound_played = play_sound(motion_types[arg_max])
                        if arg_max == 4:
                            if ser_zoom is not None:
                                ser_zoom.write(motion_types[arg_max].encode(encoding="utf-8"))
                        if arg_max == 0 or arg_max == 1:
                            if ser_swipe_lr is not None:
                                ser_swipe_lr.write(motion_types[arg_max].encode(encoding="utf-8"))
                        if arg_max == 2 or arg_max == 3:
                            if ser_swipe_ud is not None:
                                ser_swipe_ud.write(motion_types[arg_max].encode(encoding="utf-8"))
                        if arg_max == 2:
                            last_swipe = 'UP'
                        if arg_max == 3:
                            last_swipe = 'DOWN'
                        if arg_max != 2 and arg_max != 3:
                            last_swipe = ''

                    cooldown = MOTION_COOLDOWN

                # no motion, check for types
                if motion_freq[arg_max] < 1:
                    arg_max = np.argmax(type_freq)

                    # is typing
                    if type_freq[arg_max] > 2:
                        print(type_types[arg_max])
                        sound_played = play_sound(type_types[arg_max])
                        if ser_type is not None:
                            ser_type.write(type_types[arg_max].encode(encoding="utf-8"))
                        last_type = True

                    # stopped typing
                    if type_freq[arg_max] <= 2 and last_type is True:
                        print(type_types[2])
                        sound_played = play_sound(type_types[2])
                        if ser_type is not None:
                            ser_type.write(type_types[2].encode(encoding="utf-8"))
                    if type_freq[arg_max] <= 2:
                        last_type = False

        # reset frequencies
        type_freq = np.array([0, 0, 0])

        if not sound_played:
            no_sound()

    # --- DECAY MOTION FREQUENCIES
    for i in range(0, 6):
        if motion_freq[i] > 0:
            motion_freq[i] -= 1

    # --- INCREMENT VIDEO FRAME NUMBER
    count += 1

    if not success:
        end()

