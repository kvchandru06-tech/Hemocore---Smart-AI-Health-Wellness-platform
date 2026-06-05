# pdf_utils.py
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import re
import os

def extract_text_from_any_pdf(pdf_path, poppler_path=None):
    """
    Extract text from PDF using PyPDF2 first, then OCR if needed
    """
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print("Error extracting text with PyPDF2:", e)
        text = ""

    # If no text found or text is too short, try OCR
    if len(text.strip()) < 100:
        print("Text too short, trying OCR...")
        try:
            if poppler_path and os.path.exists(poppler_path):
                pages = convert_from_path(pdf_path, poppler_path=poppler_path)
            else:
                pages = convert_from_path(pdf_path)
            
            for idx, page_image in enumerate(pages):
                page_text = pytesseract.image_to_string(page_image)
                text += page_text + "\n"
                if len(text) > 1000:  # Stop if we have enough text
                    break
        except Exception as ex:
            print("OCR failed:", ex)
            return "ERROR: Could not extract text from PDF (OCR and text extraction failed)."
    
    return text

def parse_features_from_text(text):
    """
    Extract comprehensive medical parameters from blood report text
    """
    features = {}
    
    # ============ COMPREHENSIVE PATTERNS FOR ALL CONDITIONS ============
    
    # 1. COMPLETE BLOOD COUNT (CBC) PARAMETERS
    cbc_patterns = {
        'Hemoglobin': [
            r'Hemoglobin\s*\(?Hb\)?\s*[:]*\s*(\d+\.?\d*)',
            r'Hb\s*[:]*\s*(\d+\.?\d*)',
            r'Hemoglobin\s*[:]*\s*(\d+\.?\d*)'
        ],
        'RBC_COUNT': [
            r'RBC\s*(?:count)?\s*[:]*\s*(\d+\.?\d*)',
            r'Red Blood Cells\s*[:]*\s*(\d+\.?\d*)',
            r'Total RBC\s*[:]*\s*(\d+\.?\d*)'
        ],
        'PCV': [
            r'PCV\s*[:]*\s*(\d+\.?\d*)',
            r'Packed Cell Volume\s*[:]*\s*(\d+\.?\d*)',
            r'Hematocrit\s*[:]*\s*(\d+\.?\d*)'
        ],
        'MCV': [
            r'MCV\s*[:]*\s*(\d+\.?\d*)',
            r'Mean Corpuscular Volume\s*[:]*\s*(\d+\.?\d*)'
        ],
        'MCH': [
            r'MCH\s*[:]*\s*(\d+\.?\d*)',
            r'Mean Corpuscular Hemoglobin\s*[:]*\s*(\d+\.?\d*)'
        ],
        'MCHC': [
            r'MCHC\s*[:]*\s*(\d+\.?\d*)',
            r'Mean Corpuscular Hemoglobin Concentration\s*[:]*\s*(\d+\.?\d*)'
        ],
        'RDW': [
            r'RDW\s*[:]*\s*(\d+\.?\d*)',
            r'Red Cell Distribution Width\s*[:]*\s*(\d+\.?\d*)'
        ],
        'WBC_COUNT': [
            r'WBC\s*(?:count)?\s*[:]*\s*(\d+)',
            r'White Blood Cells\s*[:]*\s*(\d+)',
            r'Total WBC\s*[:]*\s*(\d+)',
            r'Leucocyte Count\s*[:]*\s*(\d+)'
        ],
        'Platelet_Count': [
            r'Platelet\s*(?:count)?\s*[:]*\s*(\d+)',
            r'Platelets\s*[:]*\s*(\d+)',
            r'Plt\s*[:]*\s*(\d+)'
        ]
    }
    
    # 2. DIFFERENTIAL WBC COUNT
    diff_patterns = {
        'Neutrophils': [
            r'Neutrophils\s*[:]*\s*(\d+)',
            r'Neutrophil\s*[:]*\s*(\d+)',
            r'Neut\.\s*[:]*\s*(\d+)'
        ],
        'Lymphocytes': [
            r'Lymphocytes\s*[:]*\s*(\d+)',
            r'Lymphocyte\s*[:]*\s*(\d+)',
            r'Lymph\.\s*[:]*\s*(\d+)'
        ],
        'Eosinophils': [
            r'Eosinophils\s*[:]*\s*(\d+)',
            r'Eosinophil\s*[:]*\s*(\d+)',
            r'Eosin\.\s*[:]*\s*(\d+)'
        ],
        'Monocytes': [
            r'Monocytes\s*[:]*\s*(\d+)',
            r'Monocyte\s*[:]*\s*(\d+)',
            r'Mono\.\s*[:]*\s*(\d+)'
        ],
        'Basophils': [
            r'Basophils\s*[:]*\s*(\d+)',
            r'Basophil\s*[:]*\s*(\d+)',
            r'Baso\.\s*[:]*\s*(\d+)'
        ]
    }
    
    # 3. LIVER FUNCTION TESTS (LFT)
    lft_patterns = {
        'ALT': [
            r'ALT\s*[:]*\s*(\d+)',
            r'Alanine Aminotransferase\s*[:]*\s*(\d+)',
            r'SGPT\s*[:]*\s*(\d+)'
        ],
        'AST': [
            r'AST\s*[:]*\s*(\d+)',
            r'Aspartate Aminotransferase\s*[:]*\s*(\d+)',
            r'SGOT\s*[:]*\s*(\d+)'
        ],
        'ALP': [
            r'ALP\s*[:]*\s*(\d+)',
            r'Alkaline Phosphatase\s*[:]*\s*(\d+)'
        ],
        'Bilirubin_Total': [
            r'Bilirubin\s*(?:Total)?\s*[:]*\s*(\d+\.?\d*)',
            r'Total Bilirubin\s*[:]*\s*(\d+\.?\d*)'
        ],
        'Bilirubin_Direct': [
            r'Bilirubin Direct\s*[:]*\s*(\d+\.?\d*)',
            r'Direct Bilirubin\s*[:]*\s*(\d+\.?\d*)'
        ],
        'Bilirubin_Indirect': [
            r'Bilirubin Indirect\s*[:]*\s*(\d+\.?\d*)',
            r'Indirect Bilirubin\s*[:]*\s*(\d+\.?\d*)'
        ],
        'Total_Protein': [
            r'Total Protein\s*[:]*\s*(\d+\.?\d*)',
            r'Protein\s*(?:Total)?\s*[:]*\s*(\d+\.?\d*)'
        ],
        'Albumin': [
            r'Albumin\s*[:]*\s*(\d+\.?\d*)'
        ],
        'Globulin': [
            r'Globulin\s*[:]*\s*(\d+\.?\d*)'
        ],
        'AG_Ratio': [
            r'A/G Ratio\s*[:]*\s*(\d+\.?\d*)',
            r'Albumin.*Globulin.*Ratio\s*[:]*\s*(\d+\.?\d*)'
        ]
    }
    
    # 4. KIDNEY FUNCTION TESTS (KFT/RFT)
    kft_patterns = {
        'Creatinine': [
            r'Creatinine\s*[:]*\s*(\d+\.?\d*)',
            r'Serum Creatinine\s*[:]*\s*(\d+\.?\d*)'
        ],
        'BUN': [
            r'BUN\s*[:]*\s*(\d+\.?\d*)',
            r'Blood Urea Nitrogen\s*[:]*\s*(\d+\.?\d*)',
            r'Urea\s*[:]*\s*(\d+\.?\d*)'
        ],
        'Uric_Acid': [
            r'Uric Acid\s*[:]*\s*(\d+\.?\d*)',
            r'Uric.*Acid\s*[:]*\s*(\d+\.?\d*)'
        ],
        'eGFR': [
            r'eGFR\s*[:]*\s*(\d+)',
            r'Estimated GFR\s*[:]*\s*(\d+)'
        ],
        'Sodium': [
            r'Sodium\s*[:]*\s*(\d+)',
            r'Na\s*[:]*\s*(\d+)'
        ],
        'Potassium': [
            r'Potassium\s*[:]*\s*(\d+\.?\d*)',
            r'K\s*[:]*\s*(\d+\.?\d*)'
        ],
        'Chloride': [
            r'Chloride\s*[:]*\s*(\d+)',
            r'Cl\s*[:]*\s*(\d+)'
        ]
    }
    
    # 5. LIPID PROFILE
    lipid_patterns = {
        'Total_Cholesterol': [
            r'Cholesterol\s*(?:Total)?\s*[:]*\s*(\d+)',
            r'Total Cholesterol\s*[:]*\s*(\d+)'
        ],
        'LDL': [
            r'LDL\s*[:]*\s*(\d+)',
            r'LDL Cholesterol\s*[:]*\s*(\d+)',
            r'Low Density Lipoprotein\s*[:]*\s*(\d+)'
        ],
        'HDL': [
            r'HDL\s*[:]*\s*(\d+)',
            r'HDL Cholesterol\s*[:]*\s*(\d+)',
            r'High Density Lipoprotein\s*[:]*\s*(\d+)'
        ],
        'Triglycerides': [
            r'Triglycerides\s*[:]*\s*(\d+)',
            r'TG\s*[:]*\s*(\d+)'
        ],
        'VLDL': [
            r'VLDL\s*[:]*\s*(\d+)',
            r'VLDL Cholesterol\s*[:]*\s*(\d+)'
        ]
    }
    
    # 6. DIABETES/THYROID (if present)
    other_patterns = {
        'Fasting_Blood_Sugar': [
            r'Fasting Blood Sugar\s*[:]*\s*(\d+)',
            r'FBS\s*[:]*\s*(\d+)',
            r'Glucose\s*(?:Fasting)?\s*[:]*\s*(\d+)'
        ],
        'PP_Blood_Sugar': [
            r'Post Prandial\s*[:]*\s*(\d+)',
            r'PPBS\s*[:]*\s*(\d+)'
        ],
        'HbA1c': [
            r'HbA1c\s*[:]*\s*(\d+\.?\d*)',
            r'Hemoglobin A1c\s*[:]*\s*(\d+\.?\d*)'
        ],
        'TSH': [
            r'TSH\s*[:]*\s*(\d+\.?\d*)',
            r'Thyroid Stimulating Hormone\s*[:]*\s*(\d+\.?\d*)'
        ],
        'T3': [
            r'T3\s*[:]*\s*(\d+\.?\d*)'
        ],
        'T4': [
            r'T4\s*[:]*\s*(\d+\.?\d*)'
        ],
        'Vitamin_D': [
            r'Vitamin D\s*[:]*\s*(\d+)',
            r'Vit.*D\s*[:]*\s*(\d+)'
        ],
        'Vitamin_B12': [
            r'Vitamin B12\s*[:]*\s*(\d+)',
            r'Vit.*B12\s*[:]*\s*(\d+)'
        ]
    }
    
    # Combine all patterns
    all_patterns = {}
    all_patterns.update(cbc_patterns)
    all_patterns.update(diff_patterns)
    all_patterns.update(lft_patterns)
    all_patterns.update(kft_patterns)
    all_patterns.update(lipid_patterns)
    all_patterns.update(other_patterns)
    
    # Extract features using all patterns
    for key, patterns in all_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    value = float(match.group(1))
                    features[key] = value
                    break  # Use first match found
                except ValueError:
                    features[key] = match.group(1)
                break
    
    # Special handling for ranges (e.g., "12.5 - 13.0")
    range_patterns = [
        (r'Hemoglobin.*?(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)', 'Hemoglobin'),
        (r'WBC.*?(\d+)\s*[-–]\s*(\d+)', 'WBC_COUNT'),
        (r'Platelet.*?(\d+)\s*[-–]\s*(\d+)', 'Platelet_Count'),
    ]
    
    for pattern, key in range_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match and key not in features:
            try:
                # Take the first value in the range
                features[key] = float(match.group(1))
            except:
                pass
    
    # Try to find values in tabular format
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Look for hemoglobin
        if ('hemoglobin' in line_lower or 'hb' in line_lower) and features.get('Hemoglobin') is None:
            # Check next few lines for numbers
            for j in range(i, min(i+3, len(lines))):
                numbers = re.findall(r'\d+\.?\d*', lines[j])
                for num in numbers:
                    try:
                        val = float(num)
                        if 5 <= val <= 20:  # Reasonable hemoglobin range
                            features['Hemoglobin'] = val
                            break
                    except:
                        pass
        
        # Similar for other key parameters
        if 'creatinine' in line_lower and features.get('Creatinine') is None:
            for j in range(i, min(i+3, len(lines))):
                numbers = re.findall(r'\d+\.?\d*', lines[j])
                for num in numbers:
                    try:
                        val = float(num)
                        if 0.1 <= val <= 10:  # Reasonable creatinine range
                            features['Creatinine'] = val
                            break
                    except:
                        pass
    
    return features

def get_feature_descriptions():
    """
    Return descriptions for all features for display
    """
    return {
        # CBC Parameters
        'Hemoglobin': 'Oxygen-carrying protein in red blood cells',
        'RBC_COUNT': 'Number of red blood cells per volume of blood',
        'PCV': 'Percentage of blood volume occupied by red cells',
        'MCV': 'Average size of red blood cells',
        'MCH': 'Average amount of hemoglobin per red cell',
        'MCHC': 'Average concentration of hemoglobin in red cells',
        'RDW': 'Variation in size of red blood cells',
        'WBC_COUNT': 'Total white blood cell count',
        'Platelet_Count': 'Number of platelets (thrombocytes)',
        
        # Differential
        'Neutrophils': 'First responders to bacterial infections',
        'Lymphocytes': 'Immune cells for viral infections and immunity',
        'Eosinophils': 'Associated with allergies and parasites',
        'Monocytes': 'Cleanup cells, become macrophages',
        'Basophils': 'Involved in allergic reactions',
        
        # Liver Function
        'ALT': 'Liver enzyme, elevated in liver damage',
        'AST': 'Liver/heart enzyme',
        'ALP': 'Liver/bone enzyme',
        'Bilirubin_Total': 'Yellow pigment from broken-down RBCs',
        
        # Kidney Function
        'Creatinine': 'Waste product, indicates kidney function',
        'BUN': 'Blood Urea Nitrogen, kidney function marker',
        'eGFR': 'Estimated Glomerular Filtration Rate',
        
        # Lipid Profile
        'Total_Cholesterol': 'Total cholesterol in blood',
        'LDL': 'Bad cholesterol, clogs arteries',
        'HDL': 'Good cholesterol, protects arteries',
        'Triglycerides': 'Fat in blood, energy storage',
        
        # Others
        'Fasting_Blood_Sugar': 'Blood glucose after fasting',
        'Vitamin_D': 'Vitamin D level, important for bones',
        'TSH': 'Thyroid Stimulating Hormone'
    }

def get_normal_ranges():
    """
    Return normal reference ranges for all features
    """
    return {
        'Hemoglobin': {'min': 13.0, 'max': 17.0, 'unit': 'g/dL', 'gender': 'Male'},
        'Hemoglobin_f': {'min': 12.0, 'max': 15.0, 'unit': 'g/dL', 'gender': 'Female'},
        'RBC_COUNT': {'min': 4.5, 'max': 5.5, 'unit': 'mill/comm'},
        'PCV': {'min': 40.0, 'max': 50.0, 'unit': '%'},
        'MCV': {'min': 83.0, 'max': 101.0, 'unit': 'fL'},
        'MCH': {'min': 27.0, 'max': 32.0, 'unit': 'pg'},
        'MCHC': {'min': 32.5, 'max': 34.5, 'unit': 'g/dL'},
        'RDW': {'min': 11.6, 'max': 14.0, 'unit': '%'},
        'WBC_COUNT': {'min': 4000, 'max': 11000, 'unit': 'cumm'},
        'Platelet_Count': {'min': 150000, 'max': 410000, 'unit': 'cumm'},
        
        # Differential ranges (%)
        'Neutrophils': {'min': 50, 'max': 62, 'unit': '%'},
        'Lymphocytes': {'min': 20, 'max': 40, 'unit': '%'},
        'Eosinophils': {'min': 0, 'max': 6, 'unit': '%'},
        'Monocytes': {'min': 0, 'max': 10, 'unit': '%'},
        'Basophils': {'min': 0, 'max': 2, 'unit': '%'},
        
        # Liver Function
        'ALT': {'min': 0, 'max': 40, 'unit': 'U/L'},
        'AST': {'min': 0, 'max': 40, 'unit': 'U/L'},
        'ALP': {'min': 44, 'max': 147, 'unit': 'U/L'},
        'Bilirubin_Total': {'min': 0.1, 'max': 1.2, 'unit': 'mg/dL'},
        
        # Kidney Function
        'Creatinine': {'min': 0.6, 'max': 1.2, 'unit': 'mg/dL', 'gender': 'Male'},
        'Creatinine_f': {'min': 0.5, 'max': 1.1, 'unit': 'mg/dL', 'gender': 'Female'},
        'BUN': {'min': 7, 'max': 20, 'unit': 'mg/dL'},
        'eGFR': {'min': 90, 'max': 120, 'unit': 'mL/min'},
        
        # Lipid Profile
        'Total_Cholesterol': {'min': 0, 'max': 200, 'unit': 'mg/dL'},
        'LDL': {'min': 0, 'max': 100, 'unit': 'mg/dL'},  # Optimal: <100
        'HDL': {'min': 40, 'max': 60, 'unit': 'mg/dL'},  # Higher is better
        'Triglycerides': {'min': 0, 'max': 150, 'unit': 'mg/dL'},
        
        # Others
        'Fasting_Blood_Sugar': {'min': 70, 'max': 100, 'unit': 'mg/dL'},
        'Vitamin_D': {'min': 30, 'max': 100, 'unit': 'ng/mL'},
        'TSH': {'min': 0.4, 'max': 4.0, 'unit': 'mIU/L'}
    }