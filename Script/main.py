import tkinter as tk
from FindClimbingRoute.FindClimbingRouteDemo import *
from FindClimbingRoute.FindClimbingRoute import *
from TrackingClimber.TrackingClimber import *

# Button functions
def button1_clicked():
    print("Find Climbing Route DEMO button clicked\n\n")
    mainFindRouteDemo()

def button2_clicked():
    print("Find Climbing Route button clicked\n\n")
    mainFindRoute()

def button3_clicked():
    print("Tracking Climber button clicked\n method: BackgroundSubtractorKNN\n\n")
    mainTrackingClimber("BackgroundSubtractorKNN")

def button4_clicked():
    print("Tracking Climber button clicked\n method: OpticalFlow\n\n")
    mainTrackingClimber("OpticalFlow")


def main():
    '''
    Main function to create the main window and the buttons
    '''

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
    labels = ["Find Climbing Route DEMO\n", "Find Climbing Route\n", "Tracking Climber (BackgroundSubtractorKNN)\n", "Tracking Climber (OpticalFlow)\n"]
    buttons = [button1_clicked, button2_clicked, button3_clicked, button4_clicked]

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
