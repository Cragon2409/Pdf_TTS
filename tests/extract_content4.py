import fitz #pip install PyMuPDF
import os

# pip install pdf2image opencv-python pytesseract
# pip install pdfplumber pdf2image opencv-python


SAVE_NAME = "test4"
SAVE_FOLDER = "saves/" + SAVE_NAME + '/'

IMAGE_FOLDER = SAVE_FOLDER + "images/"
INPUT_DEST = SAVE_FOLDER + "raw.pdf"
OUTPUT_DEST = SAVE_FOLDER + "converted_text.txt"


import os
import cv2
import fitz  # PyMuPDF
import pdfplumber
import numpy as np
from pdf2image import convert_from_path

def extract_images_with_positions(pdf_path, output_dir="extracted_images"):
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    pages = convert_from_path(pdf_path, dpi=300)  # Convert PDF pages to images

    image_positions = {}  # Store image positions per page

    for page_num, page in enumerate(pages):
        img_path = os.path.join(output_dir, f"page_{page_num+1}.png")
        page.save(img_path, "PNG")

        # Convert PIL image to OpenCV format
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        # Apply edge detection
        edges = cv2.Canny(img, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        image_positions[page_num] = []

        figure_count = 1
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # **Filter out small detections**
            if w < 100 or h < 100:  
                continue  

            # Crop and save detected figure
            figure_filename = f"figure_{page_num+1}_{figure_count}.png"
            figure_path = os.path.join(output_dir, figure_filename)
            cropped_figure = img[y:y+h, x:x+w]

            cv2.imwrite(figure_path, cropped_figure)
            image_positions[page_num].append((x, y, w, h, figure_filename))  # Store image position

            figure_count += 1

    return image_positions

def extract_text_with_images(pdf_path, image_positions):
    doc = fitz.open(pdf_path)
    full_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text() or ""  # Extract text
            
            # Get image positions for this page
            images_on_page = image_positions.get(page_num, [])

            for (x, y, w, h, filename) in images_on_page:
                text += f"\n<<{filename}>>\n"

            full_text.append(text)

    return "\n".join(full_text)






# Step 1: Extract images and their positions
image_positions = extract_images_with_positions(INPUT_DEST, IMAGE_FOLDER)

# Step 2: Extract text and insert <<image_name>> placeholders
text = extract_text_with_images(INPUT_DEST, image_positions)


with open(OUTPUT_DEST,'w',encoding="utf-8") as f:
    f.write(text)
print("File Output Written for",SAVE_NAME)