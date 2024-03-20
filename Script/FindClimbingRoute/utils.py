import cv2
import numpy as np


def find_holds(color_image, cv_image):
    """
        Finds and connects holds in an image.

        Args:
            color_image (numpy.ndarray): The color image.
            cv_image (numpy.ndarray): The OpenCV image.

        Returns:
            tuple: A tuple containing the filtered contours, center points, and the modified OpenCV image.
    """

    cv_image_ret = cv_image.copy()
    # find edges and contours
    edges = cv2.Canny(color_image, 50, 150)
    # cv2.imwrite("edges.jpg", edges)
    kernel = np.ones((3, 3), np.uint8)      # Dilate the edges to improve contour detection
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    # cv2.imwrite("dilated_edges.jpg", dilated_edges)
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours by area and non-hollow contours
    filtered_contours = []
    center_points = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 50 and cv2.contourArea(cnt) < 10000:
            filtered_contours.append(cnt)
            center = cv2.moments(cnt)
            cx = int(center["m10"] / center["m00"])
            cy = int(center["m01"] / center["m00"])
            center_points.append((cx, cy))

    # Sort the center points by y-coordinate and connect the nearest neighbors
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
            cv_image_ret = cv2.line(cv_image_ret, center_points[i], center_points[nearest_neighbor], (0, 0, 255), 2)
    
    # Draw contours on the color image
    cv_image_ret = cv2.drawContours(cv_image_ret, filtered_contours, -1, (0, 255, 0), 2)

    return filtered_contours, center_points, cv_image_ret


def find_route(center_points, cv_image):
    """
        Finds the route based on the given center points and the OpenCV image.

        Args:
            center_points (list): A list of center points.
            cv_image (numpy.ndarray): The OpenCV image.

        Returns:
            numpy.ndarray: The modified OpenCV image with the route drawn.
    """

    cv_image_ret = cv_image.copy()
    # Sort the center points by y-coordinate
    center_points = sorted(center_points, key=lambda point: point[1], reverse=True)
    mean_points = []
    temp = []
    smoothness = 6
    # create a list of mean points
    for i in range(len(center_points) + smoothness):
        if i < len(center_points):
            temp.append(center_points[i])
        if i > smoothness:
            temp.pop(0)
        intermediate_centers = [point for point in temp]
        avg_center_x = sum([point[0] for point in intermediate_centers]) / len(intermediate_centers)
        avg_center_y = sum([point[1] for point in intermediate_centers]) / len(intermediate_centers)
        mean_points.append((int(avg_center_x), int(avg_center_y)))
    
    # center_points = sorted(center_points, key=lambda point: point[1], reverse=True)
    # temp = []
    # for i in range(len(center_points)):
    #     temp.append(center_points[i])
    #     intermediate_centers = [point for point in temp]
    #     avg_center_x = sum([point[0] for point in intermediate_centers]) / len(intermediate_centers)
    #     avg_center_y = sum([point[1] for point in intermediate_centers]) / len(intermediate_centers)
    #     mean_points.append((int(avg_center_x), int(avg_center_y)))
    
    # Sort the mean points by y-coordinate
    mean_points = sorted(mean_points, key=lambda point: point[1])
    
    # Draw the route
    for i in range(len(mean_points) - 1):
        cv_image_ret = cv2.circle(cv_image_ret, (mean_points[i][0], mean_points[i][1]), 5, (255, 0, 0), -1)
        cv_image_ret = cv2.line(cv_image_ret, (int(mean_points[i][0]), int(mean_points[i][1])), (int(mean_points[i+1][0]), int(mean_points[i+1][1])), (0, 255, 255), 2)

    return cv_image_ret


def resize_img(win_width, win_height, width, height):
    """
        Resize an image to fit within a window.

        Parameters:
        win_width (int): The width of the window.
        win_height (int): The height of the window.
        width (int): The original width of the image.
        height (int): The original height of the image.

        Returns:
        tuple: A tuple containing the new width and height of the resized image.
    """
    # Set the new width and height
    win_width = win_width-270
    win_height = win_height

    # If the width is greater than the height, scale the image to fit the width of the window
    if width > height or width > win_width:
        scalingfactor = win_width/width
        new_width = win_width
        new_height = int(height*scalingfactor)
    else:
        scalingfactor = win_height/height
        new_height = win_height
        new_width = int(width*scalingfactor)
        if new_width > win_width:
            new_width = width
            new_height = height

    return new_width, new_height