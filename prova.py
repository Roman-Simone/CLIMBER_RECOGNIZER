import cv2

# Variabili globali
ix, iy = -1, -1
x1, y1 = -1, -1
drawing = False

# Funzione di callback del mouse
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

# Carica l'immagine
img = cv2.imread('Media/1_image_boulder.jpg')
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rectangle)
cv2.imshow('image', img)
while(1):
    k = cv2.waitKey(1) & 0xFF
    if k == ord('c'):  # Premi 'c' per ritagliare
        break

# Ritaglia l'immagine
print(ix, iy, x1, y1)
crop_img = img[iy:y1, ix:x1]

# Visualizza l'immagine ritagliata
cv2.imshow('crop', crop_img)
cv2.waitKey(0)
cv2.destroyAllWindows()