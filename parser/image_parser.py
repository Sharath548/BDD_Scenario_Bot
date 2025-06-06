import pytesseract
import cv2

# Set the path to the Tesseract executable (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read the image.")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()
