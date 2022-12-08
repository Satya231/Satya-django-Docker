from PIL import Image
from pytesseract import pytesseract



def extract(img_file):
    path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    img = Image.open(img_file, mode='r')
    print(img)
    pytesseract.tesseract_cmd = path_to_tesseract

    text = pytesseract.image_to_string(img)
    return text