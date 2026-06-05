from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    all_text = ""
    for page_image in pages:
        text = pytesseract.image_to_string(page_image)
        all_text += text + "\n"
    return all_text

def parse_features_from_text(text):
    import re
    features = {}
    # Sample extraction using regex: update for your report format!
    patterns = {
        "Hemoglobin": r"Hemoglobin.*?([\d.]+)",
        "Fasting_Blood_Sugar": r"Fasting Blood Sugar.*?([\d.]+)",
        "LDL": r"LDL.*?([\d.]+)",
        "HDL": r"HDL.*?([\d.]+)",
        "Triglycerides": r"Triglycerides.*?([\d.]+)",
        "Vitamin_D": r"Vitamin D.*?([\d.]+)"
    }
    for key, pat in patterns.items():
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            features[key] = float(match.group(1))
    return features
