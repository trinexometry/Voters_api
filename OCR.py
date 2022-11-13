from PIL import Image
from pytesseract import pytesseract
import time as t
from pdf2image import convert_from_path
images = convert_from_path('Data.pdf')
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
for i in range(len(images)):
    im1 = images[i]
    width, height = im1.size
    left = 69
    if (i == 0):
        top = 136
    else:
        top = 116
    right = left+1500
    bottom = top+2000
    im1 = im1.crop((left, top, right, bottom))
    # im1.show()
    left2 = 0
    top2 = 0
    bottom2 = 200
    pytesseract.tesseract_cmd = path_to_tesseract
    right2 = 500
    for j in range(0, 30):
        im2 = im1.crop((left2, top2, right2, bottom2))
        if ((j+1) % 3 == 0):
            left2 = 0
            top2 += 200
            bottom2 += 200
            right2 = 500
        else:
            left2 += 500
            right2 = left2+500
        # im2.show()
        File_object = open(r"data.txt", "a+")
        text = pytesseract.image_to_string(im2)
        offset = "\nConstituency Number 20\nSection No 1-A1\n"
        File_object.write(text[:-1])
        File_object.write("\n")
        # print(text[:-1])
        # text = ""
