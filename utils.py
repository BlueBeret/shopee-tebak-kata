import cv2
import numpy as np

def find_letters(template, img_rgb, threshold=0.9):
    w,h = template.shape[:-1]
    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)    
    
    mask = np.zeros(img_rgb.shape[:2], np.uint8)
    result = []
    for pt in zip(*loc[::-1]):
        if mask[pt[1] + int(round(h/2)), pt[0] + int(round(w/2))] != 255:
            mask[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255
            result.append((pt[0]+ w//2, pt[1]+h//2))
    
    return result


if __name__ == "__main__":
    template = cv2.imread('letters/A.png')
    img_rgb = cv2.imread('screenshot.png')

    locs = find_letters(template, img_rgb)
    print(locs)

