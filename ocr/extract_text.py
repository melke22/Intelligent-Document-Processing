# EasyOCR 
# import numpy as np
# from PIL import Image

# # Initialize reader
# reader = easyocr.Reader(['en'])

# def extract_text(image_file):

#     image = Image.open(image_file)

#     # Convert image to numpy array
#     image_np = np.array(image)

#     # OCR extraction
#     results = reader.readtext(image_np)

#     extracted_text = ""

#     for result in results:
#         extracted_text += result[1] + "\n"

#     return extracted_text 





import easyocr
import numpy as np
from PIL import Image

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def extract_text(image_file):

    image = Image.open(image_file)

    # Convert image to numpy array
    img = np.array(image)

    # OCR Extraction
    results = reader.readtext(img)

    # Extract only text
    extracted_text = ""

    for result in results:
        extracted_text += result[1] + "\n"

    return extracted_text

