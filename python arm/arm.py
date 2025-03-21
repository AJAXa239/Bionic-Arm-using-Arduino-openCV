import cv2
import mediapipe as mp
import serial

# Setup MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Setup serial communication
mySerial = serial.Serial('COM5', 9600)

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    # Convert to RGB for MediaPipe
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the image for hand landmarks
    results = hands.process(img_rgb)

    # Draw hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # List of fingers up/down (using the landmark index numbers)
            fingers = []
            # Thumb
            if results.multi_hand_landmarks[0].landmark[4].y < results.multi_hand_landmarks[0].landmark[2].y:
                fingers.append(1)
            else:
                fingers.append(0)
            # Index Finger
            if results.multi_hand_landmarks[0].landmark[8].y < results.multi_hand_landmarks[0].landmark[6].y:
                fingers.append(1)
            else:
                fingers.append(0)
            # Middle Finger
            if results.multi_hand_landmarks[0].landmark[12].y < results.multi_hand_landmarks[0].landmark[10].y:
                fingers.append(1)
            else:
                fingers.append(0)
            # Ring Finger
            if results.multi_hand_landmarks[0].landmark[16].y < results.multi_hand_landmarks[0].landmark[14].y:
                fingers.append(1)
            else:
                fingers.append(0)
            # Pinky
            if results.multi_hand_landmarks[0].landmark[20].y < results.multi_hand_landmarks[0].landmark[18].y:
                fingers.append(1)
            else:
                fingers.append(0)

            print(fingers)  # Print finger states (up/down)
            # Send the data over serial in the format $00000
            data = "$" + ''.join(map(str, fingers))  # Concatenate the finger states into a string
            mySerial.write(data.encode())

    # Show the webcam feed
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

