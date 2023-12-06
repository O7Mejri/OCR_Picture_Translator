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
   git clone https://github.com/<your-username>/OCR_Picture_Translator.git
2. Install dependencies:
    ```bash
    cd OCR_Picture_Translator
    pip install -r requirements.txt
3. Run server:
    ```bash
    python manage.py runserver
