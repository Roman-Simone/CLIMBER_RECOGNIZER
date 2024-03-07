from PIL import Image, ImageTk
import tkinter as tk
import cv2
from utils import *


# Global variable
dim_x_window = 900
dim_y_window = 800
width_form = 270
path_img = "Media/img_lead_1.jpg" #"Media/img_lead_1.jpg"  #"Media/img_lead_2.jpg"  #"Media/img_lead_3.jpg"
start_x = 0
start_y = 0
finish_x = 0
finish_y = 0
is_cropped = False
colorRGB_route = (0, 0, 0)
colorHSV_route = (0, 0, 0)

# Load the image
cv_image = cv2.cvtColor(cv2.imread(path_img), cv2.COLOR_BGR2RGB)
cv_image_backup = cv_image.copy()
hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2HSV)



def button_findRoute(canvas_image,tk_image):
    global cv_image, colorHSV_route, hsv_image, cv_image_backup

    h = colorHSV_route[0]

    lower_range = (int(h-8), 50, 50) # lower range of red color in HSV
    upper_range = (int(h+8), 255, 255) # upper range of red color in HSV


    blurred_image = cv2.GaussianBlur(hsv_image, (5, 5), 0)

    mask = cv2.inRange(blurred_image, lower_range, upper_range)
    color_image = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)



    filtered_contours, center_points, cv_image = find_holds(color_image, cv_image)

    
    cv_image = find_route(center_points, cv_image)
    cv_image_backup = cv_image.copy()

    image_tk = Image.fromarray(cv_image)

    # Converti l'immagine in formato Tkinter
    PhotoImage = ImageTk.PhotoImage(image_tk)
    canvas_image.imgref = PhotoImage
    canvas_image.itemconfig(tk_image, image=PhotoImage)

# Event handlers for the buttons
def button_cropIMG(canvas_image, tk_image, window):
    global start_x, start_y, finish_x, finish_y, is_cropped, cv_image, hsv_image, cv_image_backup

    if not is_cropped:

        # Crop the image with the dimension of rectangle
        height, width ,_= cv_image.shape
        new_w, new_h = resize_img(window.winfo_width(), window.winfo_height(), width, height)       
        cv_image = cv_image[start_y:finish_y, start_x:finish_x]

        # Resize the crop image
        height, width ,_= cv_image.shape
        new_w, new_h = resize_img(window.winfo_width(), window.winfo_height(), width, height)
        cv_image = cv2.resize(cv_image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2HSV)
        cv_image_backup = cv_image.copy()
        
        
        window.geometry(f"{new_w+width_form}x{new_h}")
    
        # Set the image on the canvas
        tk_image1 = Image.fromarray(cv_image)
        photo_image = ImageTk.PhotoImage(tk_image1)
        canvas_image.config(width=new_w, height=new_h)
        canvas_image.imgref = photo_image
        canvas_image.itemconfig(tk_image, image=photo_image)
        canvas_image.delete("rectangle")
        is_cropped = True
        
        

def update_rectangle(event, canvas_image):
    global start_x, start_y, finish_x, finish_y, is_cropped
    if not is_cropped:
        finish_x = event.x
        finish_y = event.y
        canvas_image.delete("rectangle")
        canvas_image.create_rectangle(start_x, start_y, finish_x, finish_y, outline="red", tags="rectangle")

# Funzione per ottenere il colore al click sull'immagine
def get_color(event, square_canvas, hsv_image):
    global start_x, start_y, is_cropped, colorRGB_route, colorHSV_route, cv_image

    if not is_cropped:
        start_x = event.x
        start_y = event.y
    else:
        x, y = event.x, event.y
        r, g, b = cv_image[y, x]
        h, s, v = hsv_image[y, x]
        # Crea un quadrato dello stesso colore
        colorRGB_route = (r, g, b)
        colorHSV_route = (h, s, v)
        square_size = 100
        square_image = Image.new('RGB', (square_size, square_size), colorRGB_route)
        square_photo = ImageTk.PhotoImage(square_image)
        square_canvas.create_image(0, 0, image=square_photo, anchor=tk.NW)
        square_canvas.image = square_photo

def on_resize(event, canvas_image, tk_image, window):
    # Questa funzione viene chiamata quando la finestra viene ridimensionata
    global cv_image, hsv_image, cv_image_backup
    
    height, width ,_= cv_image.shape
    new_w, new_h = resize_img(window.winfo_width(), window.winfo_height(), width, height)
    if new_w < 1 or new_h < 1:
        return
    cv_image = cv2.resize(cv_image_backup, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2HSV)
    tk_image1 = Image.fromarray(cv_image)

    # Converti l'immagine in formato Tkinter
    PhotoImage = ImageTk.PhotoImage(tk_image1)

    # Aggiorna l'immagine nel canvas
    canvas_image.config(width=new_w, height=new_h)
    canvas_image.imgref = PhotoImage

    canvas_image.itemconfig(tk_image, image=PhotoImage)


def find_route_window(window):

    # set title and dimension window
    window.title("CLIMBER RECOGNIZER")
    window.geometry(f"{dim_x_window}x{dim_y_window}")
    
    # Create a frame and a canvas for the image
    image_tk = Image.fromarray(cv_image)
    photo_image = ImageTk.PhotoImage(image_tk)
    image_frame = tk.Frame(window)
    image_frame.pack(side=tk.LEFT)
    canvas_image = tk.Canvas(image_frame)
    canvas_image.pack()

    
    tk_image = canvas_image.create_image(0, 0, image=photo_image, anchor=tk.NW)
    # Set call-back function for the canvas
    # canvas_image.bind('<Configure>', lambda event: on_resize(event, canvas_image, tk_image))
    canvas_image.bind("<Button-1>", lambda event: get_color(event, square_canvas, hsv_image))
    canvas_image.bind("<B1-Motion>", lambda event: update_rectangle(event, canvas_image))
    window.bind("<Configure>", lambda event: on_resize(event, canvas_image, tk_image, window))


    # Create a frame for buttons and labels
    frame_btn = tk.Frame(window)
    frame_btn.pack()
    label_title = tk.Label(frame_btn, text="ROUTE RECOGNIZER", font=("Arial", 20, "bold"))
    label_title.pack()

    # Button to crop the image
    button1 = tk.Button(frame_btn, text="CROP IMAGE", command=lambda: button_cropIMG(canvas_image, tk_image, window))
    button1.pack()

    label_btn1 = tk.Label(frame_btn, text="Color: ")
    label_btn1.pack()

    # Button and canvas for the color hold
    label_btn2 = tk.Label(frame_btn, text="Click the image to choose the color hold:", font=("Arial", 12))
    label_btn2.pack()
    square_canvas = tk.Canvas(frame_btn, width=100, height=100)
    colorRGB_route = (149, 20, 6)
    square_size = 100
    square_image = Image.new('RGB', (square_size, square_size), colorRGB_route)
    square_photo = ImageTk.PhotoImage(square_image)
    square_canvas.create_image(0, 0, image=square_photo, anchor=tk.NW)
    square_canvas.image = square_photo
    square_canvas.pack()
    button2 = tk.Button(frame_btn, text="DRAW THE LINE", command=lambda: button_findRoute(canvas_image, tk_image))
    button2.pack()

def mainFindRoute(flag_creation = False):

    # Create window
    if flag_creation:
        window = tk.Tk()
    else:
        window = tk.Toplevel()
    find_route_window(window)
    
    window.mainloop()


if __name__ == "__main__":

    mainFindRoute(True)

