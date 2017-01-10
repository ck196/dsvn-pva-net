import cv2
import numpy as np

def traffic_light_color(image):
    h, w, _ = image.shape

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of green color in HSV
    lower_green = np.array([60,100,100])
    upper_green = np.array([100,255,255])

    # define range of red color in HSV
    lower_red = np.array([140,100,100])
    upper_red = np.array([190,255,255])

    # define range of yellow color in HSV
    lower_yellow = np.array([0,100,100])
    upper_yellow = np.array([60,255,255])

    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    green_non_zero = np.count_nonzero(green_mask)

    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    red_non_zero = np.count_nonzero(red_mask)

    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    yellow_non_zero = np.count_nonzero(yellow_mask)
 
    # vertical


    ## GREEN
    if green_non_zero > 0 and red_non_zero == 0 and yellow_non_zero == 0:
        return 1

    ## RED
    if red_non_zero > 0 and green_non_zero == 0 and yellow_non_zero == 0:
        return 2

    ## RED
    if yellow_non_zero > 0 and green_non_zero == 0 and red_non_zero == 0:

        if w >= h:
            divide = w / 3
            center = hsv[:, divide:2*divide]
            center_yellow_mask = cv2.inRange(center, lower_yellow, upper_yellow)
            center_yellow_non_zeros = np.count_nonzero(center_yellow_mask)
            ratio = 1.0 * center_yellow_non_zeros / yellow_non_zero
            if ratio > 0.2:
                return 3
            else:
                return 2
        if h > w:
            divide = h / 3
            center = hsv[divide:2*divide,:]
            center_yellow_mask = cv2.inRange(center, lower_yellow, upper_yellow)
            center_yellow_non_zeros = np.count_nonzero(center_yellow_mask)
            ratio = 1.0 * center_yellow_non_zeros / yellow_non_zero
            if ratio > 0.2:
                return 3
            else:
                return 2
    
    if red_non_zero == 0 and green_non_zero == 0 and yellow_non_zero == 0:
        return 0
    return 0
