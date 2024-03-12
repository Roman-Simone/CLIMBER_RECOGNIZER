import cv2 
import numpy as np

# Global variables
VIDEO_PATH = "Media/video_climber.mp4"

def show(frame):
    '''
        Show the frame for debugging
    '''
    cv2.imshow("frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_bounding_box(frame, contour):
    """
        Draw a bounding box around the contour (the climber) and the center of the bounding box
        
        Args:
            frame (numpy.ndarray): The input frame/image.
            contour (numpy.ndarray): The contour of the climber.
        
        Returns:
            The frame with the bounding box and center drawn.
    """
    
    # Draw bounding box
    x, y, w, h = cv2.boundingRect(contour)

    # Check if the area is too small and adjust the size of the bounding box
    area = cv2.contourArea(contour)
    if area < 3000:
        # print("INFO: Area too small, adjusting the size of the bounding box\n")
        w = 130
        h = 130
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Draw center of the bounding box
    center_x = x + w // 2
    center_y = y + h // 2
    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
    
    return frame


def find_contours(frame):
    '''
    Find the contour of the climber (ideally the biggest one)

    Parameters:
        frame (numpy.ndarray): The input frame/image.

    Returns:
        numpy.ndarray: The contour of the climber (ideally the biggest one).
                       If no contours are found, the original frame is returned.
    '''

    countours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(countours)>0:
        max_contour = max(countours, key=cv2.contourArea)
    else:
        print("\nERROR: No contours found\n")
        return frame

    return max_contour


def opticalFlowMethod(flow, frame):
    '''
        Apply the optical flow method to the frame

        Parameters:
        - flow: numpy.ndarray, the optical flow between two consecutive frames
        - frame: numpy.ndarray, the current frame

        Returns:
        - frame: numpy.ndarray, the frame with the bounding box drawn around the detected object
    '''

    # Convert optical flow to angle and magnitude
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]

    # Calculate angle and magnitude
    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)

    # Convert angle and magnitude to HSV color space
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v*5, 255)

    # Convert HSV to BGR color space
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)



    # Convert the BGR image to grayscale
    mask = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to create a binary mask
    mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)[1]
    
    # mask = cv2.dilate(mask, np.ones((5, 5)))
    # mask = cv2.erode(mask, np.ones((5, 5)))
    #dilate and after erode the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # show(mask)

    #find contour
    contour = find_contours(mask)
    #draw bounding box
    frame = draw_bounding_box(frame, contour)

    return frame

def backSubMethod(backSub, frame):
    '''
        Apply the background subtraction method to the frame

        Parameters:
        - backSub: cv2.BackgroundSubtractor, the background subtractor object
        - frame: numpy.ndarray, the current frame

        Returns:
        - frame: numpy.ndarray, the frame with the bounding box drawn around the detected object
    '''

    # Apply Gaussian blur to the frame
    frameblur = cv2.GaussianBlur(frame, (5, 5), 0)

    # Apply background subtraction to obtain the foreground mask
    fgMask = backSub.apply(frameblur)

    # Dilate and erode the foreground mask to remove noise
    # dilatedFrame = cv2.dilate(fgMask, np.ones((5, 5)))
    # dilatedFrame = cv2.erode(dilatedFrame, np.ones((5, 5)))

    # Apply morphological closing to further refine the mask (Dilate and erode the mask)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel)

    # Find the contour of the climber 
    contour = find_contours(dilated)

    # Draw the bounding box around the climber on the frame
    frame = draw_bounding_box(frame, contour)

    # Return the modified frame
    return frame


def process_video(cap, method = "BackgroundSubtractorKNN"):
    '''
        Process the video using the specified method

        Parameters:
        - cap: cv2.VideoCapture, the video capture object
        - method: str, the method to use for tracking the climber
    '''

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Setup 
    if method == "BackgroundSubtractorKNN":
        backSub = cv2.createBackgroundSubtractorKNN(history=100, detectShadows=False)
    else:
        prevgray = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
        delay = 10
        counter = 0

    #process the video frame by frame
    while True:

        ret, frame = cap.read()
        if ret == False:
            print("INFO: End of video\n")
            break

        if method == "BackgroundSubtractorKNN":
            processed_frame = backSubMethod(backSub, frame)
        else:
            # Do optical flow every 10 frames to avoid flickering
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
    
    print("\nINFO: Processing video using method: {}\n".format(method))
    process_video(cap, method)
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    mainTrackingClimber()