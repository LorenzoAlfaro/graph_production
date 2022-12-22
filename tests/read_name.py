import cv2
import pytesseract
import numpy as np

from PIL import Image

im = Image.open("C:/Users/loren/Documents/StarCraft II/Screenshots/Screenshot2022-12-02 20_07_59.jpg")

# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size
 
# Setting the points for cropped image
left = 250
right = 500
top = 444
bottom = 470
 
# Cropped image of above dimension
# (It will not change original image)
im1 = im.crop((left, top, right, bottom))
 
# Shows the image in image viewer
# im1.show()
im1.save("./name1.jpg")


# img = cv2.imread('C:/Users/loren/Documents/StarCraft II/Screenshots/Screenshot2022-12-02 20_07_59.jpg')
img = cv2.imread('./name1.jpg')
#Alternatively: can be skipped if you have a Blackwhite image
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
gray = cv2.bitwise_not(img_bin)

pytesseract.pytesseract.tesseract_cmd = 'C:/Users/loren/AppData/Local/Tesseract-OCR/tesseract.exe'

kernel = np.ones((2, 1), np.uint8)
img = cv2.erode(gray, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=1)
out_below = pytesseract.image_to_string(img)
print("OUTPUT:", out_below)