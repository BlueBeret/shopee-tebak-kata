from datetime import datetime
import random
import pyautogui as pg
from Xlib import display
import cv2
import numpy as np
from utils import find_letters
from time import sleep
from PIL import Image
from solver import solve
from itertools import cycle

LETTER_DELAY = 0.01

def log(log_msg, *args, **kwargs):
    print("[+]", log_msg, *args, **kwargs)

def get_window_info_by_title(title):
    display_obj = display.Display()
    root = display_obj.screen().root

    window_ids = root.get_full_property(
        display_obj.intern_atom('_NET_CLIENT_LIST'),
        display.X.AnyPropertyType
    ).value

    for window_id in window_ids:
        window_obj = display_obj.create_resource_object('window', window_id)
        window_name = window_obj.get_wm_name()
        if window_name and title in window_name:
            window_geometry = window_obj.get_geometry()
            window_position = window_obj.get_geometry()
            return {
                'x': window_geometry.x,
                'y': window_geometry.y,
                'width': window_geometry.width,
                'height': window_geometry.height
            }

window_geometry = get_window_info_by_title('V2151')
print("window size is "+ str(window_geometry))

def get_all_region():
    screenshot = pg.screenshot(region=(window_geometry['x'], window_geometry['y'], window_geometry['width'], window_geometry['height']))
    all_region = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    # save screenshot 
    # cv2.imwrite(f'all_region_{datetime.now()}.png', all_region)
    return all_region
def get_input_region():
    screenshot = pg.screenshot(region=(window_geometry['x'], window_geometry['y'], window_geometry['width'], window_geometry['height']))
    input_region_screenshot = np.array(screenshot)
    input_region_screenshot[0:int(window_geometry['height']*3/4), 0:window_geometry['width']] = [0, 0, 0]
    input_region = cv2.cvtColor(input_region_screenshot, cv2.COLOR_RGB2BGR)
    return input_region

LEVEL_BOSS = {
    15 : [6, 10, 0.97],
    20 : [8, 10, 0.99],
    25 : [25, 15, 0.99],
    30 : [30, 10, 0.99]
}

level_cycle = cycle([15, 20, 25, 30])

def wait_for_level():
    while 1:
        all_region = get_all_region()
        next_template = cv2.imread('letters/!check.png')
        next_locs = find_letters(next_template, all_region)
        if len(next_locs) > 0:
            next_loc = next_locs[0]
            log("Attack button found!")
            pg.moveTo(next_loc[0] + window_geometry['x'], next_loc[1] + window_geometry['y'], LETTER_DELAY)
            pg.click()
            break

def open_boss_level(level):
    # activating window by clicking on it
    template = cv2.imread('letters/phone.png')
    img_rgb = get_all_region()

    while len(find_letters(template, img_rgb, 0.97)) == 0:
        img_rgb = get_all_region()
        sleep(0.1)

    for loc in find_letters(template, img_rgb, 0.97):
    # click
        pg.moveTo(loc[0], loc[1], 0.05)
        pg.click()
        sleep(0.1)

    log("Scrolling to level "+str(level))
    pg.scroll(LEVEL_BOSS[level][0])
    sleep(0.2)
    
    log("Opening level "+str(level))
    template = cv2.imread('letters/'+str(level)+'.png')
    img_rgb = get_all_region()
    loc = find_letters(template, img_rgb, LEVEL_BOSS[level][2], offset=LEVEL_BOSS[level][1])
    if len(loc) > 0:
        loc = loc[0]
        pg.moveTo(loc[0] + window_geometry['x'], loc[1] + window_geometry['y'], 0.05)
        pg.click()
        sleep(0.1)

        log("Clicking play button")
        while 1:
            all_region = get_all_region()
            next_template = cv2.imread('letters/!play.png')
            next_locs = find_letters(next_template, all_region)
            if len(next_locs) > 0:
                next_loc = next_locs[0]
                log("Play button found!")
                pg.moveTo(next_loc[0] + window_geometry['x'], next_loc[1] + window_geometry['y'], LETTER_DELAY)
                pg.click()
                break

        log("Waiting for level...")
        wait_for_level()
        return True
    else:
        sleep(2)
        pg.scroll(-100) 
        open_boss_level(level)

    

# save input region screenshot
def play_level():

    # open boss level
    level = level_cycle.__next__()
    open_boss_level(level)


    all_region = get_all_region()
    input_region = get_input_region()



    letters = []
    print("Finding letters...")
    
    submit_delay = 1
    

    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        try:
            # check if file exist
            open('letters/'+char+'.png')
            template = cv2.imread('letters/'+char+'.png')

            locs = find_letters(template, input_region, 0.79, offset=5)
            for loc in locs:
                letters.append((char, loc))
        except Exception as e:
            pass

        except pg.FailSafeException:
            print("Failsafe exception")
            break

    result = solve("".join([letter[0].lower() for letter in letters]))
    result.sort(key=len, reverse=True)
    print("".join([letter[0] for letter in letters]), len(result))
    for word in result:
        dup_letters = letters.copy()
        for char in word:
            for letter in dup_letters:
                if letter[0].lower() == char:
                    dup_letters.remove(letter)
                    pg.moveTo(letter[1][0] + window_geometry['x'], letter[1][1] + window_geometry['y'], LETTER_DELAY)
                    pg.click()

                    break 
    # find submit button
        submitted = False
        counter = 2
        done = False
        while not submitted:
            sleep(0.15)
            input_region = get_all_region()
            if counter == 0:
                break
            submit_template = cv2.imread('letters/!attack.png')
            submit_locs = find_letters(submit_template, input_region, offset=5)
            if len(submit_locs) > 0:
                submit_loc = submit_locs[0]
                pg.moveTo(submit_loc[0] + window_geometry['x'], submit_loc[1] + window_geometry['y'], LETTER_DELAY)
                pg.click()
                submitted = True
            counter -= 1

            ok_template = cv2.imread('letters/go_to_map.png')
            ok_locs = find_letters(ok_template, input_region)
            if len(ok_locs) > 0:
                ok_loc = ok_locs[0]
                log("Go to map button found!")
                pg.moveTo(ok_loc[0] + window_geometry['x'], ok_loc[1] + window_geometry['y'], LETTER_DELAY)
                pg.click()
                done = True
                submitted = True
                break
        
            ok_template = cv2.imread('letters/!ok.png')
            ok_locs = find_letters(ok_template, input_region)
            if len(ok_locs) > 0:
                ok_loc = ok_locs[0]
                log("OK button found!")
                pg.moveTo(ok_loc[0] + window_geometry['x'], ok_loc[1] + window_geometry['y'], LETTER_DELAY)
                pg.click()
            
        mult = 0.1
        while not submitted:
            submit_template = cv2.imread('letters/!reset.png')
            submit_locs = find_letters(submit_template, input_region, offset=5)
            if len(submit_locs) > 0:
                submit_loc = submit_locs[0]
                pg.moveTo(submit_loc[0] + window_geometry['x'], submit_loc[1] + window_geometry['y'], LETTER_DELAY)
                pg.click()
                submitted = True
                mult = 0.
            
        if done:
            break


        sleep(len(word)*0.22 * mult)
    
        # screenshot = pg.screenshot(region=(window_geometry['x'], window_geometry['y'], window_geometry['width'], window_geometry['height']))
        # all_region = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # check if done by finding ok button
                
        # ok_template = cv2.imread('letters/!ok.png')
        # ok_locs = find_letters(ok_template, all_region)
        # if len(ok_locs) > 0:
        #     ok_loc = ok_locs[0]
        #     print("Done!")
        #     pg.moveTo(ok_loc[0] + window_geometry['x'], ok_loc[1] + window_geometry['y'], LETTER_DELAY)
        #     pg.click()
        


        # # check if done by finding next button
        # next_template = cv2.imread('letters/!play.png')
        # next_locs = find_letters(next_template, all_region)
        # if len(next_locs) > 0:
        #     next_loc = next_locs[0]
        #     print("Done!")
        #     pg.moveTo(next_loc[0] + window_geometry['x'], next_loc[1] + window_geometry['y'], LETTER_DELAY)
        #     pg.click()
        #     break

if __name__ == "__main__":
    time_start = datetime.now()
    total = 0
    log("Time started: "+str(time_start))
    # do for 15 minutes, last point was 114
    while (datetime.now() - time_start).seconds < 60*60*4:
        try:
            time_start_level = datetime.now()
            play_level()
            total +=1
            print("="*20)
            log("Total time: ", str((datetime.now()- time_start).seconds//60)+" minutes " + str((datetime.now()- time_start).seconds%60)+" seconds")
            log("Time spent for this level: "+str((datetime.now()- time_start_level).seconds//60)+" minutes " + str((datetime.now()- time_start_level).seconds%60)+" seconds")
            log(f"{total} level done!")
            print("="*20)

        except Exception as e:
            print(e)
            sleep(1)
        
        except pg.FailSafeException:
            print("Failsafe exception")
            break
        