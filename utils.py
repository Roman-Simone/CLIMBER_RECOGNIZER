import cv2
from matplotlib import pyplot as plt
import os
from skimage.restoration import denoise_tv_bregman
from skimage.morphology import disk
from skimage import filters

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


























