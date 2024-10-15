import telebot
import numpy as np
import cv2
from text_extract_from_tg import image_preproc, perform_ocr, date_search, price_search

with open('config.txt', 'r') as f:
	TOKEN = f.read()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Пришлите фото чеков")

@bot.message_handler(func=lambda message: True, content_types=["photo"])
def text_handler(message):

    # Get the highest resolution photo
	photo_id = message.photo[-1].file_id

    # Get file information from the photo
	file_info = bot.get_file(photo_id)

	# Download the file
	downloaded_file = bot.download_file(file_info.file_path)

	# Convert the downloaded file to a NumPy array (OpenCV format)
	np_img = np.frombuffer(downloaded_file, np.uint8)

	# Decode the image into OpenCV format
	image = cv2.imdecode(np_img, cv2.IMREAD_GRAYSCALE)

	# Preprocess the image for better OCR
	processed_image = image_preproc(image, 843, 41)

	# Use Tesseract to extract text from the preprocessed image
	text = perform_ocr(processed_image)
	print(text)

	date = date_search(text, image)
	print(date, '1')
	price = price_search(text, image)
	print(price)

	response = f"Total: {price}\nDate: {date}"
	bot.reply_to(message, response)

bot.infinity_polling()