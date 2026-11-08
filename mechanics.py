import pytesseract
from PIL import Image

filename = 'mechanics.png'

img = Image.open(filename)
text = pytesseract.image_to_string(img)

print(f"--- TEXT FROM {filename} ---")
print(text)
print("--- END ---")
