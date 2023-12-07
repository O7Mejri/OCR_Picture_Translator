import cv2
import pytesseract
from pytesseract import Output
from googletrans import Translator
import matplotlib.pyplot as plt
import numpy as np
import urllib.request
import requests

from pdf2image import convert_from_path
import img2pdf
from reportlab.pdfgen import canvas
from PIL import Image, ImageFont, ImageDraw
import os


# Change the current working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def process(img_path, dest_lang, save_path="data\\modified_image.jpg"):
    try:
        # Cloud
        response = urllib.request.urlopen(img_path)
        img_data = response.read()
        img_array = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Local
        # img = cv2.imread(img_path)

        translator = Translator()
        dest = dest_lang

        myconf = r"--psm 11 --oem 3"
        data = pytesseract.image_to_data(img, config=myconf, output_type=Output.DICT)

        def is_empty(word):
            return word.strip() == ''
        current_block = []
        blocks = []

        for i, word in enumerate(data['text']):
            if is_empty(word):
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            else:
                current_block.append(i)

        modified_img = img.copy()

        font_path = "data/NotoSans.ttf"
        font_size = 20
        font = ImageFont.truetype(font_path, font_size)
        modified_img_pil = Image.fromarray(cv2.cvtColor(modified_img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(modified_img_pil)        

        for block in blocks:
            block_text = ' '.join(data['text'][i] for i in block)
            block_bounding_box = {
                'left': min(data['left'][i] for i in block),
                'top': min(data['top'][i] for i in block),
                'width': max(data['left'][i] + data['width'][i] for i in block) - min(data['left'][i] for i in block),
                'height': max(data['top'][i] + data['height'][i] for i in block) - min(data['top'][i] for i in block),
            }
            # source_language = translator.detect(block_text).lang
            # translated_text = translator.translate(block_text, src=source_language, dest=dest).text

            left_top = (block_bounding_box['left'], block_bounding_box['top'])
            right_bottom = (
                block_bounding_box['left'] + block_bounding_box['width'],
                block_bounding_box['top'] + block_bounding_box['height']
            )
            draw.rectangle([left_top, right_bottom], fill=(255, 255, 255))
            # text_position = (block_bounding_box['left'], block_bounding_box['top'] + block_bounding_box['height'] // 2)
            # draw.text(text_position, translated_text, font=font, fill=(0, 0, 0))

        for block in blocks:
            block_text = ' '.join(data['text'][i] for i in block)
            block_bounding_box = {
                'left': min(data['left'][i] for i in block),
                'top': min(data['top'][i] for i in block),
                'width': max(data['left'][i] + data['width'][i] for i in block) - min(data['left'][i] for i in block),
                'height': max(data['top'][i] + data['height'][i] for i in block) - min(data['top'][i] for i in block),
            }
            source_language = translator.detect(block_text).lang
            translated_text = translator.translate(block_text, src=source_language, dest=dest).text

            left_top = (block_bounding_box['left'], block_bounding_box['top'])
            right_bottom = (
                block_bounding_box['left'] + block_bounding_box['width'],
                block_bounding_box['top'] + block_bounding_box['height']
            )
            # draw.rectangle([left_top, right_bottom], fill=(255, 255, 255))
            text_position = (block_bounding_box['left'], block_bounding_box['top'])
            draw.text(text_position, translated_text, font=font, fill=(0, 0, 0))

        # Save or display the modified image
        print("DONE: ")
        # modified_img.save("data/modified_image_pil.jpg")
        # print("DONE SAVED:")
        # modified_img.show()
        # Save the modified image
        modified_img = cv2.cvtColor(np.array(modified_img_pil), cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_path, modified_img)

        print(f"Modified image saved at: {save_path}")

        return modified_img

    except Exception as e:
        print(f"Error: {str(e)}")

def processPdf(img_path, dest_lang, save_path="data\\modified_image.jpg"):
    try:
        img = cv2.imread(img_path)

        translator = Translator()
        dest = dest_lang

        myconf = r"--psm 11 --oem 3"
        data = pytesseract.image_to_data(img, config=myconf, output_type=Output.DICT)

        def is_empty(word):
            return word.strip() == ''
        current_block = []
        blocks = []

        for i, word in enumerate(data['text']):
            if is_empty(word):
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            else:
                current_block.append(i)

        modified_img = img.copy()

        font_path = "data/NotoSans.ttf"
        font_size = 20
        font = ImageFont.truetype(font_path, font_size)
        modified_img_pil = Image.fromarray(cv2.cvtColor(modified_img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(modified_img_pil)

        for block in blocks:
            block_text = ' '.join(data['text'][i] for i in block)
            block_bounding_box = {
                'left': min(data['left'][i] for i in block),
                'top': min(data['top'][i] for i in block),
                'width': max(data['left'][i] + data['width'][i] for i in block) - min(data['left'][i] for i in block),
                'height': max(data['top'][i] + data['height'][i] for i in block) - min(data['top'][i] for i in block),
            }
            # source_language = translator.detect(block_text).lang
            # translated_text = translator.translate(block_text, src=source_language, dest=dest).text

            left_top = (block_bounding_box['left'], block_bounding_box['top'])
            right_bottom = (
                block_bounding_box['left'] + block_bounding_box['width'],
                block_bounding_box['top'] + block_bounding_box['height']
            )
            draw.rectangle([left_top, right_bottom], fill=(255, 255, 255))
            # text_position = (block_bounding_box['left'], block_bounding_box['top'] + block_bounding_box['height'] // 2)
            # draw.text(text_position, translated_text, font=font, fill=(0, 0, 0))

        for block in blocks:
            block_text = ' '.join(data['text'][i] for i in block)
            block_bounding_box = {
                'left': min(data['left'][i] for i in block),
                'top': min(data['top'][i] for i in block),
                'width': max(data['left'][i] + data['width'][i] for i in block) - min(data['left'][i] for i in block),
                'height': max(data['top'][i] + data['height'][i] for i in block) - min(data['top'][i] for i in block),
            }
            source_language = translator.detect(block_text).lang
            translated_text = translator.translate(block_text, src=source_language, dest=dest).text

            left_top = (block_bounding_box['left'], block_bounding_box['top'])
            right_bottom = (
                block_bounding_box['left'] + block_bounding_box['width'],
                block_bounding_box['top'] + block_bounding_box['height']
            )
            # draw.rectangle([left_top, right_bottom], fill=(255, 255, 255))
            text_position = (block_bounding_box['left'], block_bounding_box['top'])
            draw.text(text_position, translated_text, font=font, fill=(0, 0, 0))

        # Save or display the modified image
        print("DONE: ")
        # modified_img.save("data/modified_image_pil.jpg")
        # print("DONE SAVED:")
        # modified_img.show()
        # Save the modified image
        modified_img = cv2.cvtColor(np.array(modified_img_pil), cv2.COLOR_RGB2BGR)
        print(f"Modified image saved at: {save_path}")
        cv2.imwrite(save_path, modified_img)

        return modified_img

    except Exception as e:
        print(f"Error: {str(e)}")

def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path, dpi=300)
    return images


def images_to_pdf(images, output_pdf):
    try:
        pdf = canvas.Canvas(output_pdf)
        for img_path in images:
            img = Image.open(img_path)
            width, height = img.size
            pdf.setPageSize((width, height))
            pdf.drawInlineImage(img_path, 0, 0, width, height)
            pdf.showPage()
        pdf.save()

        return output_pdf  # Return the path if successful

    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None  # Return None if an error occurs

def image_to_pdf(img_path, output_pdf):
    try:
        pdf = canvas.Canvas(output_pdf)
        img = Image.open(img_path)
        width, height = img.size
        pdf.setPageSize((width, height))
        pdf.drawInlineImage(img_path, 0, 0, width, height)
        pdf.showPage()
        pdf.save()

        return output_pdf  # Return the path if successful

    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None  # Return None if an error occurs


    
def download_pdf(url, save_path):
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(save_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        print(f"PDF downloaded successfully to {save_path}")
        return save_path
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
        return None


def run(img_path, dest_lang, save_path="data\\modified_image.jpg"):
    try:
        # PDF
        if img_path.lower().endswith(".pdf"):
            output_folder = "data"
            os.makedirs(output_folder, exist_ok=True)
            save_doc = download_pdf(img_path, 'data/pdf_doc.pdf')
            images = convert_from_path(save_doc)

            output_imgs = []
            output_imgs_paths = []
            for i, img in enumerate(images):
                page_image_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
                img.save(page_image_path)

                # Process each page
                out_img_path = f"data\\modified_image_page_{i + 1}.jpg"
                output_imgs_paths.append(out_img_path)
                out_img = processPdf(page_image_path, dest_lang, out_img_path)
                output_imgs.append(out_img)

            print("outs: ", output_imgs_paths)
            
            images = output_imgs_paths
            output_pdf = 'data/output_document1.pdf'
            generated_path = images_to_pdf(images, output_pdf)
            return generated_path, 'pdf'

        # # Docx
        # elif img_path.lower().endswith(".docx"):
        #     output_folder = "data"
        #     os.makedirs(output_folder, exist_ok=True)
        #     save_doc = download_pdf(img_path, 'data/doc_file.docx')
        #     print("saved: ", img_path)
        #     convert(img_path, 'data/pdf_doc.pdf')
        #     print("conversion: ", img_path)
        #     images = convert_from_path('data/pdf_doc.pdf')

        #     output_imgs = []
        #     output_imgs_paths = []
        #     for i, img in enumerate(images):
        #         page_image_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
        #         img.save(page_image_path)

        #         # Process each page
        #         out_img_path = f"data\\modified_image_page_{i + 1}.jpg"
        #         output_imgs_paths.append(out_img_path)
        #         out_img = processPdf(page_image_path, dest_lang, out_img_path)
        #         output_imgs.append(out_img)

        #     print("outs: ", output_imgs_paths)
            
        #     images = output_imgs_paths
        #     output_pdf = 'data/output_document1.pdf'
        #     generated_path = images_to_pdf(images, output_pdf)
        #     return generated_path, 'pdf'
        # # Doc
        # elif img_path.lower().endswith(".doc"):
        #     output_folder = "data"
        #     os.makedirs(output_folder, exist_ok=True)
        #     save_doc = download_pdf(img_path, 'data/doc_file.doc')
        #     print("saved: ", img_path)
        #     convert(img_path, 'data/pdf_doc.pdf')
        #     print("conversion: ", img_path)
        #     images = convert_from_path('data/pdf_doc.pdf')

        #     output_imgs = []
        #     output_imgs_paths = []
        #     for i, img in enumerate(images):
        #         page_image_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
        #         img.save(page_image_path)

        #         # Process each page
        #         out_img_path = f"data\\modified_image_page_{i + 1}.jpg"
        #         output_imgs_paths.append(out_img_path)
        #         out_img = processPdf(page_image_path, dest_lang, out_img_path)
        #         output_imgs.append(out_img)

        #     print("outs: ", output_imgs_paths)
            
        #     images = output_imgs_paths
        #     output_pdf = 'data/output_document1.pdf'
        #     generated_path = images_to_pdf(images, output_pdf)
        #     return generated_path, 'pdf'
            
        # Single image
        else:
            out_img = process(img_path, dest_lang, save_path)
            # print(f"Modified image saved at: {save_path}")
            return out_img, 'image'

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # imgAt = "https://esteps-dash.s3.amazonaws.com/uploads/TranslatedFile//386850987_1078924696387615_7420637516386962993_n.jpg"
    # imgAt = "data\StructAbstU.pdf"
    # imgAt = "https://www.africau.edu/images/default/sample.pdf"
    imgAt = "data/mytest.jpg"
    lang = 'fr'

    out = run(imgAt, lang)
    print(out)
