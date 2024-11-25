#~ auto-py-to-exe
#pyinstaller --noconfirm --onedir --console --icon "E:\KenzoDir_hd500\Estudos\Python\GIT\holocure_automate\automated_fish\fish_v2\holocure_fish.ico" --name "holocure-autofishing" --contents-directory "." --add-data "E:\KenzoDir_hd500\Estudos\Python\GIT\holocure_automate\automated_fish\fish_v2\fishing_module.py;." --add-data "E:\KenzoDir_hd500\Estudos\Python\GIT\holocure_automate\automated_fish\fish_v2\360p;360p/" --add-data "E:\KenzoDir_hd500\Estudos\Python\GIT\holocure_automate\automated_fish\fish_v2\images;images/"  "E:\KenzoDir_hd500\Estudos\Python\GIT\holocure_automate\automated_fish\fish_v2\holocure_fish_exe.py"#baseline
import numpy as np
import time
import datetime
#windows/screen
import ctypes
import mss
import pyautogui
import keyboard
from PIL import Image
from fishing_module import *

game_mode = ''
while game_mode not in [1,2]:
    game_mode = int(input("Choose your game mode: Fishing(1) or Cassino(2)\n"))


ctypes.windll.shcore.SetProcessDpiAwareness(2)
hwndMain = win32gui.FindWindow("YYGameMakerYY", "HoloCure")
window = win32ui.CreateWindowFromHandle(hwndMain)

if game_mode == 1:
    super_time = []
    cycle = 1
    #total_count = int(input('What is your next Chain value(last seem + 1)? 0 if reset'))
    total_count = 0
    max_chain = total_count
    level = return_level(total_count)
    screenshot = False
    #Go to pond
    goto_pond(window)
    press(window, "enter")
    
    last_press = time.perf_counter()
    while True and not keyboard.is_pressed('esc'):
        with mss.mss() as sct:
            ini = time.perf_counter()
            screen_pos = get_screen(hwndMain)
            monitor = {"left": screen_pos['left']+screen_pos['roi'][0]-level, "top": screen_pos['top']+screen_pos['roi'][1],  "width":133+level, "height": 38}
            img_src = np.array(sct.grab(monitor))
            img_rgb = cv2.cvtColor(img_src, cv2.COLOR_BGRA2RGB)
            img_rgb = cv2.resize(img_rgb, dsize=None, fx=1/screen_pos['scale'], fy=1/screen_pos['scale'],interpolation=cv2.INTER_NEAREST)
            
            #Key Press
            for key in ("space", "left", "right", "up", "down"):
                sim = get_similarity(img_rgb,key)
                if sim < 1_000:
                    press(window,keybinds[key])
                    last_press = time.perf_counter()
                    #time.sleep(0.1)
                    #Screenshot
                    if not total_count%100 and screenshot:
                        monitor_chain = {"left": screen_pos['left']+screen_pos['roi'][0]+150, "top": screen_pos['top']+screen_pos['roi'][1]-10,  "width":163, "height": 55}
                        img_chain = np.array(sct.grab(monitor_chain))
                        #img_rgb_chain = cv2.cvtColor(img_chain, cv2.COLOR_BGRA2RGB)
                        #img_rgb_chain = cv2.resize(img_rgb_chain, dsize=None, fx=1/screen_pos['scale'], fy=1/screen_pos['scale'],interpolation=cv2.INTER_NEAREST)
                        img_rgb_chain = cv2.resize(cv2.cvtColor(img_chain, cv2.COLOR_BGRA2RGB), dsize=None, fx=1/screen_pos['scale'], fy=1/screen_pos['scale'],interpolation=cv2.INTER_NEAREST)
                        #im = Image.fromarray(img_rgb_chain,mode='RGB')
                        #im.save(f'images/fish/fish_{total_count}.png')
                        Image.fromarray(img_rgb_chain,mode='RGB').save(f'images/fish/fish_{total_count}.png')
                        #print(f'Saved image: fish_{total_count}.png. Max_chain: {max_chain}')
                        screenshot = False

            #Check Failed
            monitor_failed = {"left": screen_pos['left']+screen_pos['roi'][0]-30, "top": screen_pos['top']+screen_pos['roi'][1]-130,  "width":133, "height": 38}
            img_failed = np.array(sct.grab(monitor_failed))
            img_rgb_failed = cv2.cvtColor(img_failed, cv2.COLOR_BGRA2RGB)
            img_rgb_failed = cv2.resize(img_rgb_failed, dsize=None, fx=1/screen_pos['scale'], fy=1/screen_pos['scale'],interpolation=cv2.INTER_NEAREST)
            failed = get_similarity_failed(img_rgb_failed)
            if failed <= 100:
                total_count = 0
                for i in range(2):
                    press(window, "enter")
                    time.sleep(0.02)

            #OK Press
            ok = get_similarity_ok(img_rgb)
            if ok <= 60_000_000:
                for i in range(5):
                    press(window, "enter")
                    time.sleep(0.02)
                total_count = total_count + 1
                level = return_level(total_count+1)
                #print(level)
                if total_count > max_chain:
                    max_chain = total_count
                last_press = time.perf_counter()
                screenshot = True

            #Not on Fishing Mode
            if time.perf_counter() - last_press > 15:
                press(window, "enter")
                last_press = time.perf_counter()

            #super_time.append(time.perf_counter()-ini)
            elapsed = time.perf_counter() - ini
            if elapsed < 0.01:
                time.sleep(0.01 - elapsed)

elif game_mode == 2:
    create_folder('cassino_slots')   
    last_save = time.perf_counter()
    start = 0
    print_interval = 5*60 #Minutes
    fps_limit = 30*60 #Minutes
    goto_cassino(window)
    press(window, "enter")

    ini = time.perf_counter()
    ini_fps = time.perf_counter()
    while True and not keyboard.is_pressed('esc'):
        with mss.mss() as sct:
            screen_pos = get_screen(hwndMain)
            region=(screen_pos['left'],screen_pos['top'], 640, 360)
            cassino_press(window,keybinds['space'])
            now = time.perf_counter()
            if now - last_save >= print_interval or start == 0: #keyboard.is_pressed('p')
                monitor_chain = {"left": screen_pos['left']+screen_pos['roi'][0]+220, "top": screen_pos['top']+screen_pos['roi'][1]-223,  "width":125, "height": 23}
                img_chain = np.array(sct.grab(monitor_chain))
                img_rgb_chain = cv2.cvtColor(img_chain, cv2.COLOR_BGRA2RGB)
                img_rgb_chain = cv2.resize(img_rgb_chain, dsize=None, fx=1/screen_pos['scale'], fy=1/screen_pos['scale'],interpolation=cv2.INTER_NEAREST)
                im = Image.fromarray(img_rgb_chain,mode='RGB')
                image_name = f"slots_{str(datetime.datetime.now())[0:19].replace(':','-')}.png"
                im.save(f'cassino_slots/{image_name}')
                last_save = time.perf_counter()
                start = 1
            if now >= ini_fps + fps_limit:
                reset_cassino(window,region)
                ini_fps = time.perf_counter()
    


