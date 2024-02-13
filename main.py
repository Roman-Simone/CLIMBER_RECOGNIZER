import cv2
from utils import *


if __name__ == '__main__':
    # Carica l'immagine
    img = cv2.imread('Media/1_image_boulder.jpg')
    cv2.imshow('image', img)

    # Ritaglia l'immagine
    crop_img = crop_image(img)

    # Visualizza l'immagine ritagliata
    cv2.imshow('crop', crop_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

