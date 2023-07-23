import cv2
import numpy as np

def find_letters(template, img_rgb, threshold=0.9, offset = 0, method = cv2.TM_CCOEFF_NORMED):
    w,h = template.shape[:-1]
    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)    
    
    mask = np.zeros(img_rgb.shape[:2], np.uint8)
    result = []
    for pt in zip(*loc[::-1]):
        if mask[pt[1] + int(round(h/2)), pt[0] + int(round(w/2))] != 255:
            mask[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255
            result.append((pt[0]+ w//2 + offset, pt[1]+h//2 + offset))
            # result.append((pt[0], pt[1]))
    
    return result


if __name__ == "__main__":
    # all_locs = []
    # for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    #     try:
    #         open('letters/'+char+'.png')
    #         template = cv2.imread(f'letters/{char}.png')
    #         img_rgb = cv2.imread('all_region.png')
    #         locs = find_letters(template, img_rgb, 0.79)
    #         all_locs += locs 
    #     except Exception as e:
    #         pass

    # # draw rectangle and show
    # for loc in all_locs:
    #     cv2.rectangle(img_rgb, loc, (loc[0]+template.shape[1], loc[1]+template.shape[0]), (0,255,0), 2)
    # cv2.imshow('result', img_rgb)
    # cv2.waitKey(0)
    # print(locs)

    from bot import get_all_region
    template = cv2.imread('letters/25.png')
    img_rgb = get_all_region()
    i = 0
    for loc in find_letters(template, img_rgb, 0.97):
        i += 1
        # create dot at center of letter
        cv2.circle(img_rgb, loc, 3, (0,0,255), 2)

    print(i) 
    cv2.imshow('result', img_rgb)
    cv2.waitKey(0)

