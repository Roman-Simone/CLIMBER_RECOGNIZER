import tkinter as tk
from FindClimbingRoute import *
from TrackingClimber import *

def button1_clicked():
    print("Button 1 clicked")
    mainFindRoute()

def button2_clicked():
    print("Button 2 clicked")
    mainTrackingClimber("BackgroundSubtractorKNN")

def button3_clicked():
    print("Button 3 clicked")
    mainTrackingClimber("OpticalFlow")

def main():
    # Create the main window
    main_window = tk.Tk()
    main_window.title("CLIMBER RECOGNIZER")

    # Create the grid
    grid_frame = tk.Frame(main_window)
    grid_frame.pack()

    # Create the title label
    label_title = tk.Label(grid_frame, text="CLIMBER RECOGNIZER\n\n", font=("Arial", 20, "bold"))
    label_title.grid(row=0, column=0, columnspan=2)

    # Create the labels and buttons
    labels = ["Find Climbing Route\n", "Tracking Climber (BackgroundSubtractorKNN)\n", "Tracking Climber (OpticalFlow)\n"]
    buttons = [button1_clicked, button2_clicked, button3_clicked]

    for i in range(len(labels)):
        label = tk.Label(grid_frame, text=labels[i], font=("Arial", 14, "bold"))
        label.grid(row=i+1, column=0, sticky="w")

        button = tk.Button(grid_frame, text="SUBMIT", command=buttons[i], font=("Arial", 16), relief=tk.RIDGE, bd=4)
        button.grid(row=i+1, column=1, sticky="e")

    main_window.resizable(False, False)
    # Start the main event loop
    main_window.mainloop()

if __name__ == "__main__":
    main()
