import pytesseract
import cv2
import os

# Set the path to tesseract executable (only for Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    if not os.path.exists(image_path):
        return "Error: Image file not found."

    try:
        image = cv2.imread(image_path)
        if image is None:
            return "Error: Unable to read image."

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Optional: You can improve OCR by thresholding
        # gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Extract text using pytesseract
        text = pytesseract.image_to_string(gray)

        return text.strip()
    except Exception as e:
        return f"Error during OCR: {str(e)}"
