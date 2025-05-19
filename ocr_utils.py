import pytesseract
import cv2
import os
import platform

# Sirf Windows ke liye path set karein
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    if not os.path.exists(image_path):
        return "Error: Image file not found."

    try:
        image = cv2.imread(image_path)
        if image is None:
            return "Error: Unable to read image."

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Extract text using pytesseract
        text = pytesseract.image_to_string(gray)

        return text.strip()
    except Exception as e:
        return f"Error during OCR: {str(e)}"
