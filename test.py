import numpy as np
import cv2 
from matplotlib import pyplot as plt
import os

def display(images):
    for i, image in enumerate(images):
        plt.subplot()
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), interpolation = 'bicubic')
        plt.title(i)
        plt.xticks([])
        plt.yticks([])
        plt.show()

def save(filename, images):
    for i, image in enumerate(images):
        if not os.path.exists("assets/tests"):
            os.makedirs("assets/tests")
        path = "assets/tests/{}_{}.jpg".format(filename, i)
        cv2.imwrite(path, image)


filename = "3"
img = cv2.imread('Media/2_image_lead.jpg')
orig_img = img.copy()
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgray_blur = cv2.GaussianBlur(imgray,(3,3),0)





thresh, img_bw_1 = cv2.threshold(imgray_blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
thresh, img_bw_11 = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

thresh, img_bw_2 = cv2.threshold(imgray_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
thresh, img_bw_22 = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

thresh, img_bw_3 = cv2.threshold(imgray_blur, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh, img_bw_33 = cv2.threshold(imgray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

ret, thresh = cv2.threshold(img_bw_33, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

filtered_contours = []

for contour in contours:
    area = cv2.contourArea(contour)
    
    if area > 50 and area < 500:
        filtered_contours.append(contour)

result_img = img.copy()
cv2.drawContours(result_img, filtered_contours, -1, (0,0,255), 2)

# edges = cv2.Canny(img_bw_1, threshold1=30, threshold2=100)
# ret, thresh = cv2.threshold(edges, 127, 255, 0)
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# filtered_contours = []

# for contour in contours:
#     area = cv2.contourArea(contour)
    
#     if area > 50 and area < 500:
#         filtered_contours.append(contour)

# result_img = img.copy()
# cv2.drawContours(result_img, filtered_contours, -1, (0,0,255), 2)

save(filename, [orig_img, imgray, imgray_blur, img_bw_1, img_bw_11, img_bw_2, img_bw_22, img_bw_3, img_bw_33, result_img])
# display([orig_img, imgray, imgray_blur, img_bw_1, img_bw_11, img_bw_2, img_bw_22, img_bw_3, img_bw_33, result_img])
# Applica il filtro di Canny




















