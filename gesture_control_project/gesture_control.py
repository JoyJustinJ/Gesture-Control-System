import cv2
import mediapipe as mp
import pyautogui
import os
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

def is_palm_open(hand_landmarks):
    fingers = [
        (4, 3),
        (8, 6),
        (12, 10),
        (16, 14),
        (20, 18)
    ]
    for tip, pip in fingers:
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y:
            return False
    return True

def is_palm_closed(hand_landmarks):
    fingers = [
        (8, 6),
        (12, 10),
        (16, 14),
        (20, 18)
    ]
    for tip, pip in fingers:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            return False
    return True

def is_index_up(hand_landmarks):
    return hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y

def is_middle_up(hand_landmarks):
    return hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y

def is_ring_up(hand_landmarks):
    return hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y

def is_pinky_up(hand_landmarks):
    return hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y

def is_thumb_up(hand_landmarks):
    return hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y

def is_peace_sign(hand_landmarks):
    return is_index_up(hand_landmarks) and is_middle_up(hand_landmarks) and not is_ring_up(hand_landmarks)

def is_ok_sign(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
    return distance < 0.05

def get_hand_position(hand_landmarks, frame_width, frame_height):
    wrist = hand_landmarks.landmark[0]
    x = int(wrist.x * frame_width)
    y = int(wrist.y * frame_height)
    return x, y

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    last_action_time = 0
    action_cooldown = 2
    previous_gesture = None
    previous_x = None
    previous_y = None
    swipe_threshold = 50

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        current_gesture = None
        if results.multi_hand_landmarks:
            num_hands = len(results.multi_hand_landmarks)
            if num_hands == 1:
                hand_landmarks = results.multi_hand_landmarks[0]
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                current_x, current_y = get_hand_position(hand_landmarks, frame.shape[1], frame.shape[0])
                if previous_x is not None and previous_y is not None:
                    delta_x = current_x - previous_x
                    delta_y = current_y - previous_y
                    if delta_x > 0:
                        current_gesture = "switch_left"
                    elif delta_x < 0:
                        current_gesture = "switch_right"
                    elif delta_y < -swipe_threshold:
                        current_gesture = "close_app"
                previous_x = current_x
                previous_y = current_y
                if is_palm_open(hand_landmarks) and current_gesture is None:
                    current_gesture = "open_notepad"
                elif is_peace_sign(hand_landmarks) and current_gesture is None:
                    current_gesture = "open_calculator"
                elif is_thumb_up(hand_landmarks) and current_gesture is None:
                    current_gesture = "open_browser"
                elif is_ok_sign(hand_landmarks) and current_gesture is None:
                    pass
                elif is_ring_up(hand_landmarks) and current_gesture is None:
                    current_gesture = "screenshot"
            elif num_hands == 2:
                hand1 = results.multi_hand_landmarks[0]
                hand2 = results.multi_hand_landmarks[1]
                mp_drawing.draw_landmarks(frame, hand1, mp_hands.HAND_CONNECTIONS)
                mp_drawing.draw_landmarks(frame, hand2, mp_hands.HAND_CONNECTIONS)
                if is_index_up(hand1) and is_index_up(hand2):
                    current_gesture = "minimize_window"
                elif is_middle_up(hand1) and is_middle_up(hand2):
                    current_gesture = "maximize_window"

        if current_gesture != previous_gesture and current_gesture is not None:
            current_time = time.time()
            if current_time - last_action_time > action_cooldown:
                if current_gesture == "open_notepad":
                    print("Palm open detected: Opening Notepad")
                    os.startfile('notepad.exe')
                    last_action_time = current_time
                elif current_gesture == "close_app":
                    print("Swipe up detected: Closing Active Window")
                    pyautogui.hotkey('alt', 'f4')
                    last_action_time = current_time
                elif current_gesture == "open_calculator":
                    print("Peace sign detected: Opening Calculator")
                    os.startfile('calc.exe')
                    last_action_time = current_time
                elif current_gesture == "open_browser":
                    print("Thumb up detected: Opening Browser")
                    os.startfile('chrome.exe')
                    last_action_time = current_time
                elif current_gesture == "screenshot":
                    print("Ring finger up detected: Taking Screenshot")
                    pyautogui.screenshot('screenshot.png')
                    last_action_time = current_time
                elif current_gesture == "minimize_window":
                    print("Two index fingers up detected: Minimize Window")
                    pyautogui.hotkey('win', 'down')
                    last_action_time = current_time
                elif current_gesture == "maximize_window":
                    print("Two middle fingers up detected: Maximize Window")
                    pyautogui.hotkey('win', 'up')
                    last_action_time = current_time
                elif current_gesture == "switch_left":
                    print("Swipe right detected: Switching to previous window")
                    pyautogui.hotkey('alt', 'shift', 'tab')
                    last_action_time = current_time
                elif current_gesture == "switch_right":
                    print("Swipe left detected: Switching to next window")
                    pyautogui.hotkey('alt', 'tab')
                    last_action_time = current_time
                previous_gesture = current_gesture

        cv2.imshow('Gesture Control', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
