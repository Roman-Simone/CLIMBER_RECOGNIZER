import cv2
from matplotlib import pyplot as plt
import os
from skimage.restoration import denoise_tv_bregman
from skimage.morphology import disk
from skimage import filters
import numpy as np

# Variabili globali
ix, iy = -1, -1
x1, y1 = -1, -1
drawing = False

# Function to draw the rectangle
def draw_rectangle(event, x, y, _, __):
    global ix, iy, drawing, img, x1, y1

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    if event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img2 = img.copy()
            cv2.rectangle(img2, (ix, iy), (x, y), (0, 255, 0), 1)
            cv2.imshow('image', img2)

    if event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 1)
        cv2.imshow('image', img)
        x1 = x
        y1 = y

# Function to crop the image
def crop_image(img1):
    global img
    img = img1
    cv2.setMouseCallback('image', draw_rectangle)
    while(1):
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):  # Premi 'c' per ritagliare
            break
    return img[iy+2:y1, ix+2:x1]

# Function to display the image
def display(image, title="image"):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), interpolation = 'bicubic')
    plt.title(title)
    plt.xticks([])
    plt.yticks([])
    plt.show()

# Function to save the image
def save(filename, images):
    for i, image in enumerate(images):
        if not os.path.exists("assets/tests"):
            os.makedirs("assets/tests")
        path = "assets/tests/{}_{}.jpg".format(filename, i)
        cv2.imwrite(path, image)


# Function to find countours
def find_countour(img):
    orig_img = img.copy()
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgray_blur = cv2.GaussianBlur(imgray,(3,3),0)


    thresh, img_bw_33 = cv2.threshold(imgray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    save("thresh", [img_bw_33])

    _, thresh = cv2.threshold(img_bw_33, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = []

    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > 50 and area < 500:
            filtered_contours.append(contour)

    result_img = img.copy()
    cv2.drawContours(result_img, filtered_contours, -1, (0,0,255), 2)
    return result_img, filtered_contours


def find_holds(color_image, cv_image):
    # Apply Canny edge detection and find contours
    edges = cv2.Canny(color_image, 50, 150)
    kernel = np.ones((3, 3), np.uint8)      # Dilate the edges to improve contour detection
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # Filter contours by area and non-hollow contours
    filtered_contours = []
    center_points = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 50:
            filtered_contours.append(cnt)
            center = cv2.moments(cnt)
            cx = int(center["m10"] / center["m00"])
            cy = int(center["m01"] / center["m00"])
            center_points.append((cx, cy))

    center_points = sorted(center_points, key=lambda point: point[1])
    coppie = [(0,0)]
    for i in range(len(center_points)):
        # Find the nearest neighbor for each point
        nearest_neighbor = None
        min_distance = 10000000
        for j in range(len(center_points)):
            if i != j and (i, j) not in coppie and (j, i) not in coppie and center_points[i][1] < center_points[j][1]:
                distance = np.sqrt((center_points[i][0] - center_points[j][0])**2 + (center_points[i][1] - center_points[j][1])**2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_neighbor = j
        
        # Connect the points with a line
        if nearest_neighbor is not None:
            coppie.append((i, nearest_neighbor))
            cv2.line(cv_image, center_points[i], center_points[nearest_neighbor], (0, 0, 255), 2)
    # Draw contours on the color image
    cv2.drawContours(cv_image, filtered_contours, -1, (0, 255, 0), 2)

    return filtered_contours, center_points, cv_image

def find_route(center_points, cv_image):
    # Sort center points from lowest to highest
    mean_points = []
    temp = []
    for i in range(len(center_points)):
        temp.append(center_points[i])
        intermediate_centers = [point for point in temp]
        avg_center_x = sum([point[0] for point in intermediate_centers]) / len(intermediate_centers)
        avg_center_y = sum([point[1] for point in intermediate_centers]) / len(intermediate_centers)
        mean_points.append((int(avg_center_x), int(avg_center_y)))
    
    center_points = sorted(center_points, key=lambda point: point[1], reverse=True)
    temp = []
    for i in range(len(center_points)):
        temp.append(center_points[i])
        intermediate_centers = [point for point in temp]
        avg_center_x = sum([point[0] for point in intermediate_centers]) / len(intermediate_centers)
        avg_center_y = sum([point[1] for point in intermediate_centers]) / len(intermediate_centers)
        mean_points.append((int(avg_center_x), int(avg_center_y)))
    
    mean_points = sorted(mean_points, key=lambda point: point[1])
    
    for i in range(len(mean_points) - 1):
        cv_image = cv2.circle(cv_image, (mean_points[i][0], mean_points[i][1]), 5, (255, 0, 0), -1)
        cv_image = cv2.line(cv_image, (int(mean_points[i][0]), int(mean_points[i][1])), (int(mean_points[i+1][0]), int(mean_points[i+1][1])), (0, 255, 255), 2)

    return cv_image

def resize_img(win_width, win_height, width, height):
    win_width = win_width-230
    win_height = win_height

    if width > height or width > win_width:
        scalingfactor = win_width/width
        new_width = win_width
        new_height = int(height*scalingfactor)
        print("\n----DEBUG A----")
    else:
        print("\n----DEBUG B----")
        scalingfactor = win_height/height
        new_height = win_height
        new_width = int(width*scalingfactor)
        if new_width > win_width:
            new_width = width
            new_height = height
            
    return new_width, new_height

