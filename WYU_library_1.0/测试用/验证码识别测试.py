import cv2 as cv
from PIL import Image
import pytesseract 

def recognize_text():
    src = cv.imread('D:\\WYU_library.png')
    cv.imshow("src", src)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    #kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 6))#去除线
    #binl = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    #kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 1))
    #open_out = cv.morphologyEx(binl, cv.MORPH_OPEN, kernel)
    cv.imshow('open_out', binary)

    text = pytesseract.image_to_string(binary)
    print("This OK:%s"%text)
    

    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == '__main__':
    recognize_text()