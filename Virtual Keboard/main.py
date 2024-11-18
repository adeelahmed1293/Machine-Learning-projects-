# importing the dependencies
import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep

# making a class for Buttons for showing the button on the screen
class Button:
    def __init__(self, img, pos, text, size=[85, 85]):
        self.text = text
        self.size = size
        self.pos = pos
        self.Draw(img)

    def Draw(self, img):
        x, y = self.pos
        h, w = self.size
        cv2.rectangle(img, (x, y), (x + h, y + w), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, self.text, (x + 25, y + 65), cv2.FONT_ITALIC, 2, (255, 22, 100), 2)

# Buttons list
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finalText = ""
last_pressed_key = None  # Variable to keep track of the last pressed key

# instance of the HandDetector class
hand_detector = HandDetector(detectionCon=0.8)

# Making Instance of Button class
button_list = []

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for video
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (1280, 720))  # Output file

while True:
    success, frame = cap.read()
    if not success:
        break

    hands, img = hand_detector.findHands(frame)

    # Clear button list for each frame
    button_list.clear()

    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            button_list.append(Button(img, [100 * j + 50, 100 * i + 50], key))

    if hands:
        # Information for the first hand detected
        for hand in hands:
            lmList1 = hand["lmList"]  # List of 21 landmarks for the first hand
            for button in button_list:
                x, y = button.pos
                h, w = button.size
                if x < lmList1[8][0] < x + h and y < lmList1[8][1] < y + w:
                    cv2.rectangle(img, (x, y), (x + h, y + w), (244, 30, 255), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 65), cv2.FONT_ITALIC, 2, (255, 22, 100), 2)

                    # Get coordinates of points 8 and 12
                    x1, y1 = lmList1[8][0], lmList1[8][1]
                    x2, y2 = lmList1[12][0], lmList1[12][1]

                    # Calculate Euclidean distance
                    l = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

                    # when clicked
                    if l < 30 and button.text != last_pressed_key:
                        last_pressed_key = button.text  # Update last pressed key
                        finalText += button.text
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 255), 4)
                        sleep(0.1)
                    elif l >= 30:
                        last_pressed_key = None  # Reset last pressed key when not pressed

    cv2.rectangle(img, (50, 350), (1200, 450), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Write the frame to the video file
    out.write(img)

    cv2.imshow("Image", img)  # Show the updated image with buttons and text
    if cv2.waitKey(25) == ord('q'):
        break

# Release everything if job is finished
cap.release()
out.release()  # Release the video writer
cv2.destroyAllWindows()