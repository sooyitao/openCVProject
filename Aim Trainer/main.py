import cv2
import numpy as np
import pyautogui
import os
import datetime

def pil_to_cv2(pil_image):
    open_cv_image = np.array(pil_image)
    return cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

for x in range(31):
    screenshot = pyautogui.screenshot()

    # Load an image
    gray = pil_to_cv2(screenshot)
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                param2 = 30, minRadius = 40, maxRadius = 50) 

    # Draw circles that are detected. 
    if detected_circles is not None: 
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
            pyautogui.click(a, b)
