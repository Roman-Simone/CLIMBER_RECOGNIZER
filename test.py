import cv2
import numpy as np

def button1_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Button 1 clicked!")

def button2_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Button 2 clicked!")

def main():
    # Create a black image window
    window = np.zeros((300, 300, 3), dtype=np.uint8)

    # Create button 1
    cv2.rectangle(window, (50, 100), (150, 200), (0, 255, 0), -1)
    cv2.putText(window, "Button 1", (60, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # Create button 2
    cv2.rectangle(window, (200, 100), (300, 200), (0, 0, 255), -1)
    cv2.putText(window, "Button 2", (210, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Set mouse callback functions for the buttons
    cv2.setMouseCallback("Form", button1_callback)
    cv2.setMouseCallback("Form", button2_callback)

    while True:
        cv2.imshow("Form", window)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()