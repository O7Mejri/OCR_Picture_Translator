# OCR Picture Translator

OCR Picture Translator is a Django API that utilizes Pytesseract, Google Translator, OpenCV, and PIL to take an image, extract text from it, translate the text to a specified language, and overlay the translated text on the image. The application is designed to work with images sourced from any cloud database, making it versatile and easily integrable into various projects.

## Features

- **Text Detection:** Uses Pytesseract and OpenCV for efficient text detection in images.
- **Translation:** Utilizes Google Translator to translate the detected text into the desired language.
- **Image Overlay:** Places the translated text on top of the original image for easy visualization.
- **Cloud Database Integration:** Accepts image links from any cloud database as input.

## Requirements

- Python
- Django
- Pytesseract
- Google Translator
- OpenCV
- PIL (Pillow)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/O7Mejri/OCR_Picture_Translator.git
2. Install dependencies:
    ```bash
    cd OCR_Picture_Translator
    pip install -r requirements.txt
3. Install Pytesseract:
    - Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki.

    - Install this exe in C:\Program Files (x86)\Tesseract-OCR
    - Add the file to System PATH
4. Install Poppler:
   - Download the pre-built binaries from the Poppler for Windows repository.
   - Extract the contents of the zip file.
   - Add the directory containing pdftoppm (Poppler's tool for converting PDF to images) to your system's PATH variable.
5. Install Proper GoogleTrans library:
   make sure to have this version to ensure dependency compatibilities
   ```bash
   pip install googletrans==4.0.0-rc1
4. Run server:
    ```bash
    python manage.py runserver
