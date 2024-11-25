#baseline
import os
import numpy as np
import time
import matplotlib.pyplot as plt
from math import floor

#windows/screen
import pyautogui
import win32gui
import win32ui
import win32con
import cv2
from PIL import Image
BASE_ROI = (276, 242, 133, 38)

raw = dict(
    ok=cv2.imread("./360p/ok.png", cv2.IMREAD_UNCHANGED),
    failed=cv2.imread("./360p/failed.png", cv2.IMREAD_UNCHANGED),
    space=cv2.imread("./360p/space.png", cv2.IMREAD_UNCHANGED),
    left=cv2.imread("./360p/left.png", cv2.IMREAD_UNCHANGED),
    right=cv2.imread("./360p/right.png", cv2.IMREAD_UNCHANGED),
    up=cv2.imread("./360p/up.png", cv2.IMREAD_UNCHANGED),
    down=cv2.imread("./360p/down.png", cv2.IMREAD_UNCHANGED))

templates = {}
for name, img in raw.items():
    #templates[name] = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    templates[name] = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

masks = {}
for name, img in raw.items():
    masks[name] = cv2.extractChannel(img, 3)


BUTTON = {"0": 0x30,"1": 0x31,"2": 0x32,"3": 0x33,"4": 0x34,"5": 0x35,"6": 0x36,"7": 0x37,"8": 0x38,"9": 0x39,
    "a": 0x41,"b": 0x42,"c": 0x43,"d": 0x44,"e": 0x45,"f": 0x46,"g": 0x47,"h": 0x48,"i": 0x49,"j": 0x4A,"k": 0x4B,"l": 0x4C,"m": 0x4D,
    "n": 0x4E,"o": 0x4F,"p": 0x50,"q": 0x51,"r": 0x52,"s": 0x53,"t": 0x54,"u": 0x55,"v": 0x56,"w": 0x57,"x": 0x58,"y": 0x59,"z": 0x5A,
    "space": 0x20,"enter": 0x0D,"left": 0x25,"up": 0x26,"right": 0x27,"down": 0x28,"shift": 0x10,"ctrl": 0x11,}


keybinds = {"space": "space",
            "left": "a",
            "right": "d",
            "up": "w",
            "down": "s",
            "quit":'q'}

def press(win, button_key: str):
    """Send button press to the target window."""
    #print("Pressing " + button_key)
    #button_key = button_key.lower()
    win.SendMessage(win32con.WM_KEYDOWN, BUTTON[button_key], 0)
    time.sleep(0.015)
    win.SendMessage(win32con.WM_KEYUP, BUTTON[button_key], 0)
    #time.sleep(0.015)

def cassino_press(win, button_key: str):
    """Send button press to the target window."""
    #print("Pressing " + button_key)
    #button_key = button_key.lower()
    win.SendMessage(win32con.WM_KEYDOWN, BUTTON[button_key], 0)
    time.sleep(0.007)
    win.SendMessage(win32con.WM_KEYUP, BUTTON[button_key], 0)
    time.sleep(0.007)
    #time.sleep(0.015)+

def slow_press(win, button_key: str):
    """Send button press to the target window."""
    #print("Pressing " + button_key)
    #button_key = button_key.lower()
    win.SendMessage(win32con.WM_KEYDOWN, BUTTON[button_key], 0)
    time.sleep(0.015)
    win.SendMessage(win32con.WM_KEYUP, BUTTON[button_key], 0)
    time.sleep(0.8)

def walk(win, button_key: str, duration: int):
    """Send button press to the target window."""
    #print("Pressing " + button_key)
    #button_key = button_key.lower()
    win.SendMessage(win32con.WM_KEYDOWN, BUTTON[button_key], 0)
    time.sleep(duration)
    win.SendMessage(win32con.WM_KEYUP, BUTTON[button_key], 0)
    #time.sleep(0.015)


def img_show(img):
    cv2.imshow("OpenCV/Numpy normal", img)


def show_image(image):
    """Convert OpenCV image to RGB and display using matplotlib."""
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb_image)
    plt.axis('off')  # Hide axis
    plt.show()

def save_image(image,name):
    """Convert OpenCV image to RGB and display using matplotlib."""
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.axis('off')  # Hide axis
    plt.savefig(f'{name}.png')

def create_folder(path):
    try:
        os.mkdir(path)
    except Exception as e:
        if str(e).startswith(('[WinError 183]','[Errno 17]')):
            pass
        else:
            print(e)

def get_screen(screen):
    left, top, right, bottom = win32gui.GetWindowRect(screen)
    offset_left, offset_top = win32gui.ScreenToClient(screen, (left, top))
    left = left-offset_left
    top = top - offset_top

    width, height = 640, 360
    scale = round(height / 360)
    roi = np.multiply(scale, BASE_ROI)
    return {'left':left,'top':top,'right':right,'bottom':bottom,'scale':scale,'roi':roi}

def get_similarity(img_rgb, key):
    h, w, _ = templates[key].shape
    h_offset = 10 - floor(h / 2)
    w_offset = 10 - floor(w / 2)
    res = cv2.matchTemplate(img_rgb[h_offset: h_offset + h, 103 + w_offset: 133],templates[key],cv2.TM_SQDIFF,mask= masks[key])
    min_val, _, _, _ = cv2.minMaxLoc(res)
    return min_val

def get_similarity_ok(img_rgb):
    h, w, _ = templates['ok'].shape
    res = cv2.matchTemplate(img_rgb[9: 9 + h, 0:w],templates['ok'],cv2.TM_SQDIFF,mask= masks['ok'])
    min_val, _, _, _ = cv2.minMaxLoc(res)
    return min_val

def get_similarity_failed(img_rgb):
    h, w, _ = templates['failed'].shape
    res = cv2.matchTemplate(img_rgb,templates['failed'],cv2.TM_SQDIFF,mask= masks['failed'])
    min_val, _, _, _ = cv2.minMaxLoc(res)
    return min_val

def return_level(chain):
    return min(7, int(chain/10))


def reset_cassino(window,region):
    while not image_exist(f'360p/spin.png',region):
        slow_press(window,keybinds['space'])
        time.sleep(1)
    time.sleep(10)
    slow_press(window,keybinds['quit'])
    slow_press(window,keybinds['quit'])
    slow_press(window,keybinds['up'])
    slow_press(window,keybinds['space']) 
    slow_press(window,keybinds['space']) 
    time.sleep(3)#Transition
    slow_press(window,keybinds['space']) 
    slow_press(window,keybinds['space']) 
    slow_press(window,keybinds['space']) 
    slow_press(window,keybinds['right'])#select house
    slow_press(window,keybinds['space']) 
    slow_press(window,keybinds['space']) 
    time.sleep(3)#Transition
    walk(window,keybinds['right'],3)
    walk(window,keybinds['up'],0.7)
    slow_press(window,keybinds['space']) 

def goto_pond(window):
    slow_press(window,keybinds['right'])
    slow_press(window,keybinds['space']) #select House
    slow_press(window,keybinds['space']) #select Character
    slow_press(window,keybinds['space']) #select Outfit
    slow_press(window,keybinds['space']) #select Enter House 
    slow_press(window,keybinds['space']) #Go
    walk(window,keybinds['left'],3)
    return

def goto_cassino(window):
    slow_press(window,keybinds['right'])
    slow_press(window,keybinds['space']) #select House
    slow_press(window,keybinds['space']) #select Character
    slow_press(window,keybinds['space']) #select Outfit
    slow_press(window,keybinds['right'])
    slow_press(window,keybinds['space']) #select Enter Cassino 
    slow_press(window,keybinds['space']) #Go
    walk(window,keybinds['right'],3)
    walk(window,keybinds['up'],0.7)
    return

def image_exist(file,region):
    try:
        x,y= pyautogui.locateCenterOnScreen(file,grayscale=True, confidence=0.8,region=region)
        return True
    except Exception as e:
        print(e)
        return False