# pip install pdf2image opencv-python pytesseract
# pip install pdfplumber pdf2image opencv-python




import os
import cv2
import fitz  # PyMuPDF
import pdfplumber
import numpy as np
import shutil
from pdf2image import convert_from_path

def extract_images_with_positions(pdf_path, output_dir):
    if os.path.exists(output_dir):
        print("Existing Images Deleted from",output_dir)
        shutil.rmtree(output_dir)
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

def extract_pdf_text(pdf_path, image_positions):
    doc = fitz.open(pdf_path)
    main_text = []
    image_count = 1

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        page_text = []
        
        for block in blocks:
            
            rotation = block.get("rotation", 0)
            
            # If the block is not oriented upright (rotation != 0), skip it
            if rotation != 0:
                continue

            if "lines" in block:
                # Detect table-like structures: Many short, aligned text chunks
                # if len(block["lines"]) > 5 and all(len(line["spans"]) > 1 for line in block["lines"]):
                #     continue  # Skip tables

                # Get the rotation of the block (0 means upright, 90 means rotated, etc.)

                for line in block["lines"]:
                    text_spans = [(span["text"], span["size"], span["flags"]) for span in line["spans"]]
                    text = " ".join([span[0] for span in text_spans]).strip()
                    
                    # Skip headers/footers (top/bottom 5% of page)
                    if block["bbox"][1] < page.rect.height * 0.05 or block["bbox"][3] > page.rect.height * 0.95:
                        continue
                    
                    # Skip figure captions
                    # if text.startswith(("Figure", "Fig.")):
                    #     continue
                    
                    # Detect headings (heuristic: larger font size)
                    font_sizes = [span[1] for span in text_spans]
                    max_font_size = max(font_sizes) if font_sizes else 0
                    if max_font_size > 12:  # Adjust threshold as needed
                        text = f"<<Title:{text}>>"

                    page_text.append(text)
                page_text.append('\n')
        
        # Get image positions for this page
        images_on_page = image_positions.get(page_num, [])

        for (x, y, w, h, filename) in images_on_page:
            text += f"\n<<Image:{filename}>>\n"

        page_text.append(text)
        
        main_text.append(" ".join(page_text))
        

    return "\n<<NewPage>>\n".join(main_text)





def convert_file(save_name):
    save_folder = "saves/" + save_name + '/'
    image_folder = save_folder + "images/"
    input_dest = save_folder + "raw.pdf"
    output_dest = save_folder + "converted_text.txt"

    # Step 1: Extract images and their positions
    image_positions = extract_images_with_positions(input_dest, image_folder)

    # Step 2: Extract text and insert <<image_name>> placeholders
    text = extract_pdf_text(input_dest, image_positions)

    #Write file output
    with open(output_dest,'w',encoding="utf-8") as f:
        f.write(text)
    print("File Output Written for",SAVE_NAME)

    #Detect Number of Pages
    page_num = text.count("<<NewPage>>")
    print("Output has",page_num,"pages")
    manifest_dest = save_folder + '/manifest.txt'

    #Read Manifest Info
    with open(manifest_dest, 'r') as f:
        manifest_lines = f.read().splitlines()
    original_location = ':'.join(manifest_lines[1].split(':')[1:])

    #Rewrite Manifest Info
    manifest_content = '\n'.join([
        "converted:true",
        "original_path:" + original_location,
        "pages:" + str(page_num)
    ])
    with open(manifest_dest,'w') as f:
        f.write(manifest_content)
    print("Rewrote Manifest")

if __name__ == "__main__":
    SAVE_NAME = "D4RL"
    convert_file(SAVE_NAME)