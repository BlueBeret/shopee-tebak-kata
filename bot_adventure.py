from datetime import datetime
import pyautogui as pg
from Xlib import display
import cv2
import numpy as np
from utils import find_letters
from time import sleep
from PIL import Image
from solver import solve

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


# save input region screenshot
def play_level():
    all_region = get_all_region()
    input_region = get_input_region()
    # save input region screenshot
    cv2.imwrite('input_region.png', input_region)



    letters = []
    print("Finding letters...")
    letter_delay = 0.05
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
    result = solve("".join([letter[0].lower() for letter in letters]))
    result.sort(key=len, reverse=True)
    print("".join([letter[0] for letter in letters]), len(result))
    for word in result:
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
        counter = 5
        while not submitted:
            input_region = get_all_region()
            if counter == 0:
                break
            submit_template = cv2.imread('letters/!attack.png')
            submit_locs = find_letters(submit_template, input_region, offset=5)
            if len(submit_locs) > 0:
                submit_loc = submit_locs[0]
                print("Submitted word: "+word)
                pg.moveTo(submit_loc[0] + window_geometry['x'], submit_loc[1] + window_geometry['y'], letter_delay)
                pg.click()
                submitted = True
            sleep(0.25)
            counter -= 1
        done = False
        while not submitted:
            submit_template = cv2.imread('letters/!reset.png')
            submit_locs = find_letters(submit_template, input_region, offset=5)
            if len(submit_locs) > 0:
                submit_loc = submit_locs[0]
                print("Submitted word: "+word)
                pg.moveTo(submit_loc[0] + window_geometry['x'], submit_loc[1] + window_geometry['y'], letter_delay)
                pg.click()
                submitted = True
            
            screenshot = pg.screenshot(region=(window_geometry['x'], window_geometry['y'], window_geometry['width'], window_geometry['height']))
            all_region = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)



            ok_template = cv2.imread('letters/!next_level.png')
            ok_locs = find_letters(ok_template, all_region)
            if len(ok_locs) > 0:
                ok_loc = ok_locs[0]
                print("Done!")
                pg.moveTo(ok_loc[0] + window_geometry['x'], ok_loc[1] + window_geometry['y'], letter_delay)
                pg.click()
        
            ok_template = cv2.imread('letters/!ok.png')
            ok_locs = find_letters(ok_template, all_region)
            if len(ok_locs) > 0:
                ok_loc = ok_locs[0]
                print("Done!")
                pg.moveTo(ok_loc[0] + window_geometry['x'], ok_loc[1] + window_geometry['y'], letter_delay)
                pg.click()
            
            # check if done by finding next button
            next_template = cv2.imread('letters/!play.png')
            next_locs = find_letters(next_template, all_region)
            if len(next_locs) > 0:
                next_loc = next_locs[0]
                print("Done!")
                pg.moveTo(next_loc[0] + window_geometry['x'], next_loc[1] + window_geometry['y'], letter_delay)
                pg.click()
                done = True
                break
        
        if done:
            break


        sleep(len(word)*0.22)
    
        screenshot = pg.screenshot(region=(window_geometry['x'], window_geometry['y'], window_geometry['width'], window_geometry['height']))
        all_region = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # check if done by finding ok button
        ok_template = cv2.imread('letters/!next_level.png')
        ok_locs = find_letters(ok_template, all_region)
        if len(ok_locs) > 0:
            ok_loc = ok_locs[0]
            print("Done!")
            pg.moveTo(ok_loc[0] + window_geometry['x'], ok_loc[1] + window_geometry['y'], letter_delay)
            pg.click()
        
        ok_template = cv2.imread('letters/!ok.png')
        ok_locs = find_letters(ok_template, all_region)
        if len(ok_locs) > 0:
            ok_loc = ok_locs[0]
            print("Done!")
            pg.moveTo(ok_loc[0] + window_geometry['x'], ok_loc[1] + window_geometry['y'], letter_delay)
            pg.click()
        


        # check if done by finding next button
        next_template = cv2.imread('letters/!play.png')
        next_locs = find_letters(next_template, all_region)
        if len(next_locs) > 0:
            next_loc = next_locs[0]
            print("Done!")
            pg.moveTo(next_loc[0] + window_geometry['x'], next_loc[1] + window_geometry['y'], letter_delay)
            pg.click()
            break
    else:
        print("done by loop, waiting for button")
    # check if done by finding ok button
        count = 0
        while 1:
            if count > 10:
                raise("Cannot find OK button")
            count += 1
            all_region = get_all_region()            
            ok_template = cv2.imread('letters/!next_level.png')
            ok_locs = find_letters(ok_template, all_region)
            if len(ok_locs) > 0:
                ok_loc = ok_locs[0]
                print("Done!")
                pg.moveTo(ok_loc[0] + window_geometry['x'], ok_loc[1] + window_geometry['y'], letter_delay)
                pg.click()
        
            all_region = get_all_region()            
            ok_template = cv2.imread('letters/!ok.png')
            ok_locs = find_letters(ok_template, all_region)
            if len(ok_locs) > 0:
                ok_loc = ok_locs[0]
                print("Done!")
                pg.moveTo(ok_loc[0] + window_geometry['x'], ok_loc[1] + window_geometry['y'], letter_delay)
                pg.click()
        


        # check if done by finding next button
            next_template = cv2.imread('letters/!play.png')
            next_locs = find_letters(next_template, all_region)
            if len(next_locs) > 0:
                next_loc = next_locs[0]
                print("Done!")
                pg.moveTo(next_loc[0] + window_geometry['x'], next_loc[1] + window_geometry['y'], letter_delay)
                sleep(0.5)
                pg.click()
                break
            sleep(1)


if __name__ == "__main__":
    while 1:
        try:
            play_level()
            # wait until check button appear
            print("Waiting for level...")
            while 1:
                all_region = get_all_region()
                check_template = cv2.imread('letters/!check.png')
                check_locs = find_letters(check_template, all_region)
                if len(check_locs) > 0:
                    check_loc = check_locs[0]
                    print("Check!")
                    pg.moveTo(check_loc[0] + window_geometry['x'], check_loc[1] + window_geometry['y'], 0.2)
                    break
                sleep(1)
        except Exception as e:
            print(e)
            sleep(1)
        
        except pg.FailSafeException:
            print("Failsafe exception")
            break
        