import unittest
import cv2
from text_extract_from_tg import image_preproc, perform_ocr, date_search, price_search

class TestPerformOcr(unittest.TestCase):
    """dddd"""
    def test_perform_ocr(self):
        img = cv2.imread("../pikchi/photo_2024-07-29_12-33-00 (2).jpg", cv2.IMREAD_GRAYSCALE)
        preprocesed_img = image_preproc(img, 843, 41)
        recognized_text = perform_ocr(preprocesed_img)
        date = date_search(recognized_text, img)
        price = price_search(recognized_text, img)

        self.assertEqual(f"{date}, {price}", "24.07.2024, 11.44")

if __name__ == '__main__':
    unittest.main()
