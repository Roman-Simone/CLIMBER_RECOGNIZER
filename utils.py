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

def crop_image(img1):
    global img
    img = img1
    cv2.setMouseCallback('image', draw_rectangle)
    while(1):
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):  # Premi 'c' per ritagliare
            break
    return img[iy:y1, ix:x1]