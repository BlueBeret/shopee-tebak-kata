import pyautogui as pg
from Xlib import display
import ewmh
import cv2
import numpy as np
from utils import find_letters
from time import sleep
from PIL import Image

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

screenshot = pg.screenshot(region=(window_geometry['x'], window_geometry['y'], window_geometry['width'], window_geometry['height']))

# input region is lower 1/4 of screenshot
# fill non input region with black
input_region_screenshot = np.array(screenshot)
input_region_screenshot[0:int(window_geometry['height']*3/4), 0:window_geometry['width']] = [0, 0, 0]

# save input region screenshot
input_region = cv2.cvtColor(input_region_screenshot, cv2.COLOR_RGB2BGR)

all_region = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

letters = []
print("Finding letters...")

for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    try:
        # check if file exist
        open('letters/'+char+'.png')
        template = cv2.imread('letters/'+char+'.png')
        locs = find_letters(template, input_region, 0.97)
        for loc in locs:
            letters.append((char, loc))
    except Exception as e:
        pass
from solver import solve
result = solve("".join([letter[0].lower() for letter in letters]))
print(result)
letter_delay = 0.2
submit_delay = 1
sleep(0.5)
for word in result:
    # stop program if ctrl + alt is pressed
    dup_letters = letters.copy()
    for char in word:
        for letter in dup_letters:
            if letter[0].lower() == char:
                dup_letters.remove(letter)
                pg.moveTo(letter[1][0] + window_geometry['x'], letter[1][1] + window_geometry['y'], letter_delay)
                pg.click()

                break 
    # find submit button
    submitted = False
    while not submitted:
        submit_template = cv2.imread('letters/submit.png')
        submit_locs = find_letters(submit_template, input_region)
        if len(submit_locs) > 0:
            submit_loc = submit_locs[0]
            print("Submitted word: "+word)
            pg.moveTo(submit_loc[0] + window_geometry['x'], submit_loc[1] + window_geometry['y'], letter_delay)
            pg.click()
            submitted = True

    sleep(len(word)*0.22 + 0.3)
    
    screenshot = pg.screenshot(region=(window_geometry['x'], window_geometry['y'], window_geometry['width'], window_geometry['height']))
    all_region = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # check if done by finding ok button
    ok_template = cv2.imread('letters/OK.png')
    ok_locs = find_letters(ok_template, all_region)
    if len(ok_locs) > 0:
        ok_loc = ok_locs[0]
        print("Done!")
        pg.moveTo(ok_loc[0] + window_geometry['x'], ok_loc[1] + window_geometry['y'], letter_delay)
        pg.click()
        

    # check if done by finding next button
    next_template = cv2.imread('letters/next_level.png')
    next_locs = find_letters(next_template, all_region)
    if len(next_locs) > 0:
        next_loc = next_locs[0]
        print("Done!")
        pg.moveTo(next_loc[0] + window_geometry['x'], next_loc[1] + window_geometry['y'], letter_delay)
        pg.click()
        break

else:
    # check if done by finding ok button
    while 1:
        screenshot = pg.screenshot(region=(window_geometry['x'], window_geometry['y'], window_geometry['width'], window_geometry['height']))
        all_region = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        print("Finding OK button...") 
        ok_template = cv2.imread('letters/OK.png')
        ok_locs = find_letters(ok_template, all_region)
        if len(ok_locs) > 0:
            ok_loc = ok_locs[0]
            print("Done!")
            pg.moveTo(ok_loc[0] + window_geometry['x'], ok_loc[1] + window_geometry['y'], letter_delay)
            pg.click()
        

    # check if done by finding next button
        next_template = cv2.imread('letters/next_level.png')
        next_locs = find_letters(next_template, all_region)
        if len(next_locs) > 0:
            next_loc = next_locs[0]
            print("Done!")
            pg.moveTo(next_loc[0] + window_geometry['x'], next_loc[1] + window_geometry['y'], letter_delay)
            sleep(0.5)
            pg.click()
            break
        sleep(1)

