import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import tempfile

def extract_text_from_pdf(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text.strip()

def extract_text_from_image_pdf(path):
    text = ""
    with tempfile.TemporaryDirectory() as temp_dir:
        images = convert_from_path(path, output_folder=temp_dir)
        for image in images:
            text += pytesseract.image_to_string(image)
    return text.strip()
