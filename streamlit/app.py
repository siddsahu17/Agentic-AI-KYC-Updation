import streamlit as st
import re
import pytesseract
from paddleocr import PaddleOCR
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import pypdfium2 as pdfium
from PIL import Image
import numpy as np
import io

# NOTE: 
# 1. Tesseract binary must be installed separately and added to PATH. 
#    Or set: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# 2. pypdfium2 is used for PDF to image conversion (no system dependency needed).

st.set_page_config(page_title="Aadhaar OCR Extraction Demo", layout="wide")

st.title("Aadhaar OCR Extraction Demo")
st.markdown("Upload an Aadhaar card PDF to compare extraction results from multiple OCR engines.")

# --- OCR Functions ---

@st.cache_resource
def load_paddle():
    # Initialize PaddleOCR
    return PaddleOCR(use_angle_cls=True, lang='en')

@st.cache_resource
def load_trocr():
    # Initialize TrOCR
    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed')
    return processor, model

def ocr_tesseract(images):
    text_output = ""
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        text_output += f"--- Page {i+1} ---\n{text}\n\n"
    return text_output

def ocr_paddle(images, ocr_engine):
    text_output = ""
    for i, img in enumerate(images):
        # PaddleOCR expects numpy array
        img_np = np.array(img)
        result = ocr_engine.ocr(img_np)
        text_output += f"--- Page {i+1} ---\n"
        if result and result[0]:
            for line in result[0]:
                text_output += line[1][0] + "\n"
        text_output += "\n"
    return text_output

def ocr_trocr(images, processor, model):
    text_output = ""
    for i, img in enumerate(images):
        pixel_values = processor(images=img.convert("RGB"), return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        text_output += f"--- Page {i+1} ---\n{generated_text}\n\n"
    return text_output

import re

# ... (imports remain same)

# ... (load functions remain same)

def extract_fields(text):
    """
    Simple heuristic to extract Name and ID Number (PAN or Aadhaar).
    """
    data = {"ID Number": None, "Name": None, "Type": "Unknown"}
    
    # Cleaning
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # 1. ID Number Detection
    # PAN Regex: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)
    pan_match = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', text)
    
    # Aadhaar Regex: 12 digits, often spaced (e.g., 1234 5678 9012)
    aadhaar_match = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', text)
    
    if pan_match:
        data["ID Number"] = pan_match.group(0)
        data["Type"] = "PAN Card"
    elif aadhaar_match:
        data["ID Number"] = aadhaar_match.group(0)
        data["Type"] = "Aadhaar Card"

    # 2. Name Detection
    # Logic: Look for lines after "Name" or "GOVT OF INDIA"
    # This is very basic and specific to the card layout
    for i, line in enumerate(lines):
        # PAN Card heuristic: Name often comes after "Name" or "INCOME TAX DEPARTMENT" block
        if "Name" in line and i + 1 < len(lines):
            # Check if next line is not another label
            candidate = lines[i+1]
            if "Father" not in candidate and "Date" not in candidate:
                data["Name"] = candidate
                break
        
        # Fallback: Look for all caps name (3 parts) if type is PAN
        if data["Type"] == "PAN Card" and not data["Name"]:
            # Ignore headers
            if "GOVT" in line or "INDIA" in line or "INCOME" in line or "TAX" in line or "Card" in line:
                continue
            # Assume 3 words, uppercase is a name
            if re.match(r'^[A-Z]+\s[A-Z]+\s[A-Z]+$', line):
                 data["Name"] = line
                 break

    return data

# ... (ocr wrapper functions remain same)

# --- UI Logic ---

uploaded_file = st.file_uploader("Upload Document (Aadhaar/PAN PDF)", type="pdf")

if uploaded_file:
    with st.spinner("Converting PDF to images..."):
        try:
            # Convert PDF to images using pypdfium2
            pdf = pdfium.PdfDocument(uploaded_file.getvalue())
            images = []
            for i in range(len(pdf)):
                page = pdf[i]
                # Increase scale to 4 (approx 300 DPI) for better OCR accuracy
                bitmap = page.render(scale=4) 
                pil_image = bitmap.to_pil()
                images.append(pil_image)
            
            st.success(f"PDF converted successfully. {len(images)} pages found.")
            
            # Display images preview
            with st.expander("View Document Images"):
                cols = st.columns(len(images))
                for i, img in enumerate(images):
                    cols[i].image(img, caption=f"Page {i+1}", use_column_width=True)

        except Exception as e:
            st.error(f"Error converting PDF: {e}")
            st.stop()

    tab1, tab2, tab3 = st.tabs(["Tesseract OCR", "PaddleOCR", "TrOCR"])

    with tab1:
        st.header("Tesseract OCR")
        if st.button("Run Tesseract"):
            with st.spinner("Running Tesseract..."):
                try:
                    text = ocr_tesseract(images)
                    st.text_area("Raw Extracted Text", text, height=300)
                    
                    st.subheader("Extracted Details")
                    details = extract_fields(text)
                    st.json(details)
                    
                except Exception as e:
                    st.error(f"Tesseract Failed: {e}. Check if Tesseract is installed and in PATH.")

    with tab2:
        st.header("PaddleOCR")
        if st.button("Run PaddleOCR"):
            with st.spinner("Running PaddleOCR..."):
                try:
                    paddle_engine = load_paddle()
                    text = ocr_paddle(images, paddle_engine)
                    st.text_area("Raw Extracted Text", text, height=300)
                    
                    st.subheader("Extracted Details")
                    details = extract_fields(text)
                    st.json(details)
                    
                except Exception as e:
                    st.error(f"PaddleOCR Failed: {e}")

    with tab3:
        st.header("TrOCR (HuggingFace)")
        st.info("Note: TrOCR relies on a heavy model and might be slow on CPU.")
        if st.button("Run TrOCR"):
            with st.spinner("Loading Model & Running TrOCR..."):
                try:
                    processor, model = load_trocr()
                    text = ocr_trocr(images, processor, model)
                    st.text_area("Raw Extracted Text", text, height=300)
                    
                    st.subheader("Extracted Details")
                    details = extract_fields(text)
                    st.json(details)
                    
                except Exception as e:
                    st.error(f"TrOCR Failed: {e}")

else:
    st.info("Please upload a PDF file to begin.")
