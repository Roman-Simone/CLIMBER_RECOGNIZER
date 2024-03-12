# CLIMBER_RECOGNIZER


<div>
     <img src="https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54" alt="Python"/>
     <img src="https://img.shields.io/badge/opencv-3670A0?style=flat&logo=opencv" alt="Python"/>
     <img src="https://img.shields.io/badge/numpy-3670A0?style=flat&logo=numpy" alt="Python"/>
</div>



## Table of contents

-   [Description](#Description)
-   [Installation](#Installation)
-   [Running the project](#Running-the-project)

## Description
This project has two goals:
- The first is to create software capable of recognizing an indoor climbing route given a photo given the color of the route holds
- The second to perform tracking of a climber using a video as input. Two modes were used the first is with optical flow while the second is with bgbackground

To simulate this, a graphical user interface was created with python's tkinter library.

#### Results recognize climbing route
<center>
    <div align="center">
        <img src="Media/img_lead_2_crop.jpg" style="width: 10%; margin-right: 20px; text-align: center">
        <img src="Media/img_lead_2_crop_processed.jpg" style="width: 10%;">
    </div>
</center>

#### Results tracking climber

<center>

<img src="Media/My-Movie-4.gif" style="width: 50%;" align="center">

</center>

## Installation

In order to run the project you'll need to clone it and install the requirements. We suggest you to create a virtual environment 
- Clone it

    ```BASH
    git clone https://github.com/Roman-Simone/CLIMBER_RECOGNIZER.git
    ```
- Create the virtual environment 
  
    ```BASH
    python -m venv name_of_virtual_env
    ```
- Activate the virtual environment
    ```BASH
    source name_of_virtual_env/bin/activate
    ```
- Install the requirements
    ```BASH
    pip install -r requirements.txt
    ```

## Running the project

The project can be runned in two different ways:
- through the GUI:
  
    ```BASH
    python main.py
    ```
    After running it a menu will be opened there select the demo you want to try out.
    

- Running directly:
  
    - To run the find route part:
        ```
        python FindClimbingRoute.py
        ```
    - To run the Tracking Climber part:
        ```
        python TrackingClimber.py
        ```
        N.B. if you want to change the method change the string



# Contacts

Simone Roman - [simone.roman@studenti.unitn.it](mailto:simone.roman@studenti.unitn.it)

<a href="https://www.unitn.it/"><img src="https://ing-gest.disi.unitn.it/wp-content/uploads/2022/11/marchio_disi_bianco_vert_eng-1024x295.png" width="300px"></a>
