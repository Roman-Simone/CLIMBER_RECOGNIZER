from PIL import Image, ImageTk
import tkinter as tk
import cv2
import os
import sys
if os.path.basename(sys.argv[0]) == "main.py":
    from FindClimbingRoute.utils import *
else:
    from utils import *

# Global variable
dim_x_window = 900  # Dim x window standard
dim_y_window = 800  # Dim y window standard
width_form = 270    # Width of the form
path_img = "Media/img_lead_1.jpg" #"Media/img_lead_1.jpg"  #"Media/img_lead_2.jpg" 
start_x = -1  # Start x coordinate of the rectangle
start_y = -1  # Start y coordinate of the rectangle
finish_x = -1 # Finish x coordinate of the rectangle
finish_y = -1 # Finish y coordinate of the rectangle
is_cropped = False    # Flag to check if the image is cropped
colorHSV_route = (0, 0, 0)   # HSV color of the route
# Elements of the form
button_crop, label_button_crop, button_find_route, square_canvas, label_button_fRoute, button_resett = None, None, None, None, None, None


# Load the image
cv_image = cv2.cvtColor(cv2.imread(path_img), cv2.COLOR_BGR2RGB)
cv_image_backup = cv_image.copy()
hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2HSV)


def button_reset(window):
    '''
        Function to reset the window
    '''
    global cv_image, hsv_image, cv_image_backup, button_crop, label_button_crop, button_find_route, square_canvas, label_button_fRoute, is_cropped, button_resett, path_img
    
    # Reset the image
    cv_image = cv2.cvtColor(cv2.imread(path_img), cv2.COLOR_BGR2RGB)
    cv_image_backup = cv_image.copy()
    hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2HSV)
    
    is_cropped = False # Reset the flag

    # Reset the form
    label_button_crop.pack()
    button_crop.pack()
    label_button_fRoute.pack_forget()
    square_canvas.pack_forget()
    button_find_route.pack_forget()
    button_resett.pack_forget()
    window.geometry(f"{dim_x_window}x{dim_y_window}")


def button_findRoute(canvas_image, tk_image):
    '''
        Finds and displays the climbing route on the canvas.

        Parameters:
        - canvas_image: The canvas object where the image is displayed.
        - tk_image: The image object on the canvas.

        Returns:
        None
    '''
    global cv_image, colorHSV_route, hsv_image, cv_image_backup

    h = colorHSV_route[0]

    lower_range = (int(h-7), 50, 50) # lower range of red color in HSV
    upper_range = (int(h+7), 255, 255) # upper range of red color in HSV

    blurred_image = cv2.GaussianBlur(hsv_image, (5, 5), 0)

    # Create the mask for the holds
    mask = cv2.inRange(blurred_image, lower_range, upper_range)
    mask = cv2.threshold(cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), 1, 255, cv2.THRESH_BINARY)[1]
    mask = cv2.dilate(mask, None, iterations=2)

    # Find the holds and the route
    _, center_points, cv_image = find_holds(mask, cv_image)
    cv_image = find_route(center_points, cv_image)
    cv_image_backup = cv_image.copy()

    # Convert the image to Tkinter format
    PhotoImage = ImageTk.PhotoImage(Image.fromarray(cv_image))
    canvas_image.imgref = PhotoImage
    canvas_image.itemconfig(tk_image, image=PhotoImage)


def button_cropIMG(canvas_image, tk_image, window):
    """
        Crop the image based on the coordinates of a rectangle and update the canvas with the cropped image.

        Parameters:
        canvas_image (tkinter.Canvas): The canvas widget where the image is displayed.
        tk_image (int): The image item on the canvas.
        window (tkinter.Tk): The main window of the application.

        Returns:
        None
    """
    global start_x, start_y, finish_x, finish_y, is_cropped, cv_image, hsv_image, cv_image_backup, button_crop, label_button_crop, button_find_route, square_canvas, label_button_fRoute, button_resett

    # Check if the image was already cropped
    if not is_cropped:
        # Check if the rectangle was drawn
        if start_x > 0 and start_y > 0 and finish_x > 0 and finish_y > 0:

            # Crop the image with the dimension of rectangle
            height, width ,_= cv_image.shape
            new_w, new_h = resize_img(window.winfo_width(), window.winfo_height(), width, height)       
            cv_image = cv_image[start_y:finish_y, start_x:finish_x]

            # Resize the crop image
            height, width ,_= cv_image.shape
            new_w, new_h = resize_img(window.winfo_width(), window.winfo_height(), width, height)
            cv_image = cv2.resize(cv_image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
            hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2HSV)
            cv_image_backup = cv_image.copy()
            
            # Resize the window
            window.geometry(f"{new_w+width_form}x{new_h}")
        
            # Set the image on the canvas
            photo_image = ImageTk.PhotoImage(Image.fromarray(cv_image))
            canvas_image.config(width=new_w, height=new_h)
            canvas_image.imgref = photo_image
            canvas_image.itemconfig(tk_image, image=photo_image)
            canvas_image.delete("rectangle")

        # Update the form
        label_button_crop.pack_forget()
        button_crop.pack_forget()
        label_button_fRoute.pack()
        square_canvas.pack()
        button_find_route.pack(side = tk.LEFT, padx = 10, pady = 10)
        button_resett.pack(side = tk.RIGHT, padx = 10, pady = 10)

        # Set the flag
        is_cropped = True


def update_rectangle(event, canvas_image):
    """
        Update the rectangle on the canvas based on the event coordinates.

        Parameters:
        - event: The event object containing the coordinates of the mouse click.
        - canvas_image: The canvas object where the rectangle is drawn.
    """
    global start_x, start_y, finish_x, finish_y, is_cropped
    if not is_cropped:
        finish_x = event.x
        finish_y = event.y
        # Delete the previous rectangle
        canvas_image.delete("rectangle")
        # Draw the new rectangle
        canvas_image.create_rectangle(start_x, start_y, finish_x, finish_y, outline="red", tags="rectangle")


def get_color(event, square_canvas, hsv_image):
    """
        Retrieves the color information from the specified event coordinates in the canvas.

        Parameters:
        - event (tkinter.Event): The event object containing the coordinates of the mouse click.
        - square_canvas (tkinter.Canvas): The canvas where the square image will be displayed.
        - hsv_image (numpy.ndarray): The HSV image from which the color information will be retrieved.

        Returns:
        None
    """
    global start_x, start_y, is_cropped, colorRGB_route, colorHSV_route, cv_image

    # Check if the image was already cropped
    if not is_cropped:
        start_x = event.x
        start_y = event.y
    else:
        # Get the color information from the HSV image
        x, y = event.x, event.y
        r, g, b = cv_image[y, x]
        h, s, v = hsv_image[y, x]
        print(f"H: {h}, S: {s}, V: {v}")
        colorRGB_route = (r, g, b)
        colorHSV_route = (h, s, v)
        
        # Create a square image with the selected color
        square_size = 100
        square_image = Image.new('RGB', (square_size, square_size), colorRGB_route)
        square_photo = ImageTk.PhotoImage(square_image)
        square_canvas.create_image(0, 0, image=square_photo, anchor=tk.NW)
        square_canvas.image = square_photo


def on_resize(event, canvas_image, tk_image, window):
    """
    This function is called when the window is resized.
    
    Args:
        event: The event object that triggered the resize.
        canvas_image: The canvas image object.
        tk_image: The Tkinter image object.
        window: The Tkinter window object.
    """
    global cv_image, hsv_image, cv_image_backup
    
    # Resize the image
    height, width ,_= cv_image.shape
    new_w, new_h = resize_img(window.winfo_width(), window.winfo_height(), width, height)
    if new_w < 1 or new_h < 1:
        return
    # Resize the image
    cv_image = cv2.resize(cv_image_backup, (new_w, new_h), interpolation=cv2.INTER_AREA)
    hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2HSV)

    # Convert the image to Tkinter format
    PhotoImage = ImageTk.PhotoImage(Image.fromarray(cv_image))

    # Update the image in the canvas
    canvas_image.config(width=new_w, height=new_h)
    canvas_image.imgref = PhotoImage
    canvas_image.itemconfig(tk_image, image=PhotoImage)


def find_route_window(window):
    """
        This function sets up the main window for the Climber Recognizer application.
        
        Parameters:
            window (tkinter.Tk): The main window object.
        
        Returns:
            None
    """
    global button_crop, label_button_crop, button_find_route, square_canvas, label_button_fRoute, button_resett
    
    # set title and dimension window
    window.title("CLIMBER RECOGNIZER")
    window.geometry(f"{dim_x_window}x{dim_y_window}")
    
    # Create a frame and a canvas for the image
    photo_image = ImageTk.PhotoImage(Image.fromarray(cv_image))
    image_frame = tk.Frame(window)
    image_frame.pack(side=tk.LEFT)
    canvas_image = tk.Canvas(image_frame)
    canvas_image.pack()
    tk_image = canvas_image.create_image(0, 0, image=photo_image, anchor=tk.NW)
    # Set call-back function for the canvas
    canvas_image.bind("<Button-1>", lambda event: get_color(event, square_canvas, hsv_image))
    canvas_image.bind("<B1-Motion>", lambda event: update_rectangle(event, canvas_image))
    window.bind("<Configure>", lambda event: on_resize(event, canvas_image, tk_image, window))

    # Create a frame for buttons and labels
    frame_btn = tk.Frame(window)
    frame_btn.pack()
    label_title = tk.Label(frame_btn, text="ROUTE RECOGNIZER", font=("Arial", 20, "bold"))
    label_title.pack()

    # Button to crop the image
    label_button_crop = tk.Label(frame_btn, text="INFO: Click and drag to draw the area\n of interest after click to crop the image.", font=("Arial", 12))
    button_crop = tk.Button(frame_btn, text="CROP IMAGE", command=lambda: button_cropIMG(canvas_image, tk_image, window))
    label_button_crop.pack()
    button_crop.pack()

    # Button and canvas for the color hold
    label_button_fRoute = tk.Label(frame_btn, text="INFO: Click on the image to choose the\n color then click find route to draw the route:", font=("Arial", 12))
    square_canvas = tk.Canvas(frame_btn, width=100, height=100)
    colorRGB_route = (149, 20, 6)
    square_size = 100
    square_image = Image.new('RGB', (square_size, square_size), colorRGB_route)
    square_photo = ImageTk.PhotoImage(square_image)
    square_canvas.create_image(0, 0, image=square_photo, anchor=tk.NW)
    square_canvas.image = square_photo
    button_find_route = tk.Button(frame_btn, text="DRAW THE LINE", command=lambda: button_findRoute(canvas_image, tk_image))
    button_resett = tk.Button(frame_btn, text="RESET", command=lambda: button_reset(window))


def mainFindRoute(flag_creation=False):
    """
        Main function for finding climbing routes.

        Args:
            flag_creation (bool): Flag indicating whether to create a new window or use a top-level window.

        Returns:
            None
    """

    if flag_creation:
        window = tk.Tk()
    else:
        window = tk.Toplevel()
    find_route_window(window)
    
    window.mainloop()


if __name__ == "__main__":
    
    mainFindRoute(True)