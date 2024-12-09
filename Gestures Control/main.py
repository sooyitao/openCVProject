import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_y = 0  # For scrolling
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0].landmark
        index_finger_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
        
        # Gesture: Scroll
        if prev_y and abs(index_finger_tip.y - prev_y) > 0.02:  # Sensitivity threshold
            if index_finger_tip.y < prev_y:
                print("Scrolling Up")
                pyautogui.scroll(10)
            else:
                print("Scrolling Down")
                pyautogui.scroll(-10)
        prev_y = index_finger_tip.y
        
        # Gesture: Click
        distance = ((index_finger_tip.x - thumb_tip.x)**2 + (index_finger_tip.y - thumb_tip.y)**2)**0.5
        if distance < 0.05:  # Adjust threshold
            print("Click!")
            pyautogui.click()

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
