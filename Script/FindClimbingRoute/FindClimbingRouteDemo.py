import cv2
import matplotlib.pyplot as plt
from FindClimbingRoute.utils import *
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt




# Global variable
path_img1 = "Media/img_lead_2_crop.jpg"
path_img2 = "Media/img_lead_1_crop.jpg" 


def find_route_demo():
    '''
        Function to create two plot to show climbing route recognition
    '''
    global path_img1, path_img2

    lower_range_red = (1, 50, 50) # lower range of red color in HSV
    upper_range_red = (10, 255, 255) # upper range of red color in HSV
    lower_range_green = (50, 0, 0) # lower range of green color in HSV
    upper_range_green = (70, 255, 255) # upper range of green color in HSV
    lower_range_blue = (105, 50, 50) # lower range of blue color in HSV
    upper_range_blue = (115, 255, 255) # upper range of blue color in HSV

    # Create patches with the desired colors for legend
    green_patch = mpatches.Patch(color=(0,1,0), label='Climbing Holds')
    blue_patch = mpatches.Patch(color=(0,0,1), label='Holds connection')
    light_blue_patch = mpatches.Patch(color=(0, 1, 1), label='Route')
    
    # Load the first image and process it
    cv_image = cv2.cvtColor(cv2.imread(path_img1), cv2.COLOR_BGR2RGB)
    blurred_image = cv2.GaussianBlur(cv_image, (5, 5), 0)
    hsv_image = cv2.cvtColor(blurred_image, cv2.COLOR_RGB2HSV)
    
    # Create the mask for the red holds
    mask = cv2.inRange(hsv_image, lower_range_red, upper_range_red)
    mask = cv2.threshold(cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), 1, 255, cv2.THRESH_BINARY)[1]

    # Find the holds and the route
    _, center_points, cv_image_processed_1 = find_holds(mask, cv_image)
    cv_image_processed_1 = find_route(center_points, cv_image_processed_1)

    # Create the mask for the green holds
    mask = cv2.inRange(hsv_image, lower_range_green, upper_range_green)
    mask = cv2.threshold(cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), 1, 255, cv2.THRESH_BINARY)[1]
    mask = cv2.dilate(mask, None, iterations=2)

    # Find the holds and the route
    _, center_points, cv_image_processed_2 = find_holds(mask, cv_image)
    cv_image_processed_2 = find_route(center_points, cv_image_processed_2)

    # Show first plot
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 7))
    
    fig.suptitle('Find Climbing Route Demo 1', fontsize=16, fontweight='bold')

    ax1.imshow(cv_image)
    ax1.set_title('Original Image')
    ax1.axis('off')

    ax2.imshow(cv_image_processed_1)
    ax2.set_title('Processed Image Red Route')
    ax2.axis('off')

    ax3.imshow(cv_image_processed_2)
    ax3.set_title('Processed Image Green Route')
    ax3.axis('off')

    fig.legend(handles=[light_blue_patch, blue_patch, green_patch], loc='upper center', bbox_to_anchor=(0.5, 0.94), ncol=3, fontsize='small')
    plt.subplots_adjust(top=0.85)    
    plt.show()

    # Load the second image and process it
    cv_image = cv2.cvtColor(cv2.imread(path_img2), cv2.COLOR_BGR2RGB)
    blurred_image = cv2.GaussianBlur(cv_image, (5, 5), 0)
    hsv_image = cv2.cvtColor(blurred_image, cv2.COLOR_RGB2HSV)
    
    # Create the mask for the blue holds
    mask = cv2.inRange(hsv_image, lower_range_blue, upper_range_blue)
    mask = cv2.threshold(cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), 1, 255, cv2.THRESH_BINARY)[1]
    mask = cv2.dilate(mask, None, iterations=2)

    # Find the holds and the route
    _, center_points, cv_image_processed = find_holds(mask, cv_image)
    cv_image_processed = find_route(center_points, cv_image_processed)

    # Show second plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))
    fig.suptitle('Find Climbing Route Demo 2', fontsize=16, fontweight='bold')

    ax1.imshow(cv_image)
    ax1.set_title('Original Image')
    ax1.axis('off')

    ax2.imshow(cv_image_processed)
    ax2.set_title('Processed Image Blue Route')
    ax2.axis('off')

    fig.legend(handles=[light_blue_patch, blue_patch, green_patch], loc='upper center', bbox_to_anchor=(0.5, 0.94), ncol=3, fontsize='small')
    plt.subplots_adjust(top=0.85)
    plt.show()


def mainFindRouteDemo():

    find_route_demo()



if __name__ == "__main__":

    mainFindRouteDemo()