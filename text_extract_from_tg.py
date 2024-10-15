import re
from collections import Counter
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

custom_config = r'--oem 3 --psm 6'

counter = 0

# preparing image for reading
def image_preproc(original_image, block_size, c):
    adaptive = cv2.adaptiveThreshold(original_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c)

    return adaptive

#lets find the price of the category.
def price_search(text, image):
    print('hui')
    price=re.findall(r'\b\w{5}\b\s*[:\s]*[^\d\s]*\s*(\d+[\,\.]\d{2})', text)
    print(price)
    if not price:
        print('1')
    else:
        print('o') 
    price_list = list(map(float,price))
    print(price_list)
    print(max(price_list))
    if max(price_list) > 90:
        pro_img = image_preproc(image, 843, 41)
        text = pytesseract.image_to_string(pro_img, config=custom_config)     
        price = price_search(text)
        return price
    elif price == []:
        price = 'цена не найдена, попробуйте другое фото'
        return price
    else:
        return max(price_list)

#lets find the date of the receipt.
def date_search(text,image):
    global counter
    dates = re.findall(r'\b\d{2}[\/\.]\d{2}[\/\.]\d{2,4}\b', text)
    if dates == []:
        pro_img = image_preproc(image, 843, 41)
        text = pytesseract.image_to_string(pro_img, config=custom_config)
        
        if counter == 0:
            counter += 1 
            date = date_search(text, pro_img)
        else:
            date = 'дата не найдена, попробуйте другое фото'
            print(date, '0')
            return date
    else:
        date = Counter(dates).most_common(1)[0][0]
        date = date.replace('/','.')
        return date

def perform_ocr(image):
    return pytesseract.image_to_string(image, config=custom_config)

