import cv2
import mediapipe as mp

# Initialize mediapipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=1)

# Emoji mapping
def get_emoji(fingers):
    if fingers == [0, 1, 0, 0, 0]:
        return "☝️"
    elif fingers == [0, 1, 1, 0, 0]:
        return "✌️"
    elif fingers == [0, 1, 1, 1, 0]:
        return "🤟"
    elif fingers == [1, 1, 1, 1, 1]:
        return "🖐️"
    elif fingers == [0, 0, 0, 0, 0]:
        return "✊"
    else:
        return "🤔"

# Finger detection logic
def detect_fingers(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for tip in tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            fingers = detect_fingers(handLms)
            emoji = get_emoji(fingers)

            cv2.putText(img, emoji, (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 3,
                        (0, 255, 0), 3)

    cv2.imshow("Hand Gesture Emoji", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()