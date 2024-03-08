import cv2 
import numpy as np
from utils import *


# Global variables
VIDEO_PATH = "Media/video_climber.mp4"
point_for_line = []

def show(frame):
    cv2.imshow("frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_bounding_box(frame, contour):
    global point_for_line


    # Draw bounding box
    x, y, w, h = cv2.boundingRect(contour)
    area = cv2.contourArea(contour)
    if area < 3000:
        print("Area too small")
        w = 130
        h = 130
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Draw center of the bounding box
    center_x = x + w // 2
    center_y = y + h // 2
    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
    point_for_line.append((center_x, center_y))
    # Fit a non-linear regression lin
    # Connect points with a line without regression
    # frame = find_route(point_for_line, frame)
    
    return frame




def find_contours(frame):
    countours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(countours)>0:
        max_contour = max(countours, key=cv2.contourArea)
    else:
        print("No contours found")
        return frame

    return max_contour





def opticalFlowMethod(flow, frame):

    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]

    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)

    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v*4, 255)
    #colore giallo hsv
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    mask = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)[1]
    
    mask = cv2.dilate(mask, np.ones((5, 5)))
    mask = cv2.erode(mask, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # show(mask)
    contour = find_contours(mask)

    frame = draw_bounding_box(frame, contour)

    return frame

def backSubMethod(backSub, frame):

    frameblur = cv2.GaussianBlur(frame, (5, 5), 0)

    fgMask = backSub.apply(frameblur)
    
    dilatatedFrame = cv2.dilate(fgMask, np.ones((5, 5)))
    dilatatedFrame = cv2.erode(dilatatedFrame, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.morphologyEx(dilatatedFrame, cv2.MORPH_CLOSE, kernel)

    countour = find_contours(dilated)

    frame = draw_bounding_box(frame, countour)
    
    return frame


def process_video(cap, method = "BackgroundSubtractorKNN"):
    fps = cap.get(cv2.CAP_PROP_FPS)

    if method == "BackgroundSubtractorKNN":
        backSub = cv2.createBackgroundSubtractorKNN(history=100, detectShadows=False)
    else:
        prevgray = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
        delay = 10
        counter = 0


    while True:

        ret, frame = cap.read()
        if ret == False:
            break
        
        if method == "BackgroundSubtractorKNN":
            processed_frame = backSubMethod(backSub, frame)
        else:
            if counter < delay:
                counter += 1
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                continue
            counter = 0
            flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            prevgray = gray
            processed_frame = opticalFlowMethod(flow, frame)

        cv2.imshow('processed_video', processed_frame)
        
        if cv2.waitKey(int(1000/fps)) & 0xFF == ord("q"):
            break


def mainTrackingClimber(method = "BackgroundSubtractorKNN"):
    # open video
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Error opening video stream or file")
        return
    process_video(cap, method)
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    mainTrackingClimber()