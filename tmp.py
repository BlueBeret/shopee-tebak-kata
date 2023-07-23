import time
import pyautogui as pg
import cv2

from bot import get_all_region
from utils import find_letters

template = cv2.imread('letters/phone.png')
img_rgb = get_all_region()

for loc in find_letters(template, img_rgb, 0.97):
    # click
    pg.moveTo(loc[0], loc[1], 0.05)
    pg.click()
    time.sleep(0.3)

# scroll up 
# pg.scroll(6) # buat ke 15
# pg.scroll(8) # buat ke 20
pg.scroll(25) # buat ke 25
time.sleep(0.3)

template = cv2.imread('letters/30.png')
img_rgb = get_all_region()

for loc in find_letters(template, img_rgb, 0.99, offset=10):
    # click
    pg.moveTo(loc[0], loc[1], 0.05)
    time.sleep(0.5)
    pg.click()
    print("done")

{
    15 : [6, 10, 0.97],
    20 : [8, 10, 0.99],
    25 : [25, 15, 0.97],
    30 : [30, 10, 0.99]
}

# 21249
# 12733
# 10789
