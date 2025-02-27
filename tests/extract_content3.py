import fitz #pip install PyMuPDF
import os

# pip install pdf2image opencv-python pytesseract


SAVE_NAME = "test3"
SAVE_FOLDER = "saves/" + SAVE_NAME + '/'

IMAGE_FOLDER = SAVE_FOLDER + "images/"
INPUT_DEST = SAVE_FOLDER + "raw.pdf"
OUTPUT_DEST = SAVE_FOLDER + "converted_text.txt"



import os
import cv2
import numpy as np
from pdf2image import convert_from_path

def extract_pdf_text(pdf_path, output_dir="extracted_figures"):
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

    # Convert PDF pages to images (high DPI for accuracy)
    pages = convert_from_path(pdf_path, dpi=300)

    for page_num, page in enumerate(pages):
        img_filename = f"page_{page_num+1}.png"
        img_path = os.path.join(output_dir, img_filename)

        # Save full page image
        page.save(img_path, "PNG")

        # Convert PIL image to OpenCV format
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        # Apply edge detection to find figures
        edges = cv2.Canny(img, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        figure_count = 1
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # **Filter out small contours (likely noise)**
            if w < 100 or h < 100:  # Adjust threshold as needed
                continue  

            # Crop and save detected figure
            figure_filename = f"figure_{page_num+1}_{figure_count}.png"
            figure_path = os.path.join(output_dir, figure_filename)
            cropped_figure = img[y:y+h, x:x+w]

            cv2.imwrite(figure_path, cropped_figure)
            print(f"Extracted Figure: {figure_path}")

            figure_count += 1





text = extract_pdf_text(INPUT_DEST, IMAGE_FOLDER)
# text = text.encode("utf-8")
with open(OUTPUT_DEST,'w',encoding="utf-8") as f:
    f.write(text)

print("File Output Written")
