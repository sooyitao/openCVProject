import cv2
import numpy as np
import pyautogui
import os
import datetime

# Take a screenshot and save it
subfolder_name = 'screenshots'
current_directory = os.getcwd()
folder_path = os.path.join(current_directory, subfolder_name)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f'Error deleting file {file_path}: {e}')

for x in range(31):
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(folder_path, f'screenshot_{timestamp}.png')
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)

    # Load an image
    img = cv2.imread(screenshot_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                param2 = 30, minRadius = 40, maxRadius = 60) 

    # Draw circles that are detected. 
    if detected_circles is not None: 
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
            pyautogui.click(a, b)
