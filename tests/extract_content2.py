import fitz #pip install PyMuPDF
import os




SAVE_NAME = "test3"
SAVE_FOLDER = "saves/" + SAVE_NAME + '/'

IMAGE_FOLDER = SAVE_FOLDER + "images/"
INPUT_DEST = SAVE_FOLDER + "raw.pdf"
OUTPUT_DEST = SAVE_FOLDER + "converted_text.txt"



def extract_pdf_text(pdf_path, output_image_dir=IMAGE_FOLDER):
    doc = fitz.open(pdf_path)
    os.makedirs(output_image_dir, exist_ok=True)  # Ensure output directory exists
    main_text = []
    image_count = 1

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        page_text = []
        
        for block in blocks:
            if "lines" in block:
                # Detect table-like structures: Many short, aligned text chunks
                # if len(block["lines"]) > 5 and all(len(line["spans"]) > 1 for line in block["lines"]):
                #     continue  # Skip tables

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
        
        # Extract images and insert placeholders
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]  # Image reference ID
            img_data = doc.extract_image(xref)
            img_bytes = img_data["image"]
            img_ext = img_data["ext"]
            img_filename = f"image_{page_num+1}_{image_count}.{img_ext}"
            img_path = os.path.join(output_image_dir, img_filename)
            img_width = img_data.get("width", 0)
            img_height = img_data.get("height", 0)

            if img_width < 50 or img_height < 50:  # Adjust threshold if needed
                continue  # Skip tiny images (likely icons)

            # Save the extracted image
            with open(img_path, "wb") as img_file:
                img_file.write(img_bytes)

            # Insert placeholder in text
            page_text.append(f"<<Image:{img_filename}>>")
            image_count += 1
        
        # **Alternative method: Extract missing images from figures**
        
        main_text.append(" ".join(page_text))

    return "\n".join(main_text)




text = extract_pdf_text(INPUT_DEST)
# text = text.encode("utf-8")
with open(OUTPUT_DEST,'w',encoding="utf-8") as f:
    f.write(text)

print("File Output Written")
