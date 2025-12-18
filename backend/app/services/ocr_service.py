from paddleocr import PaddleOCR
import logging

# Initialize PaddleOCR (downloads model on first run)
# use_angle_cls=True helps with rotated images
# lang='en' because Aadhaar usually has English text we care about
ocr = PaddleOCR(use_angle_cls=True, lang='en')

logger = logging.getLogger(__name__)

def extract_text(file_path: str) -> str:
    """
    Runs OCR on Aadhaar image or PDF and returns raw text.
    """
    try:
        logger.info(f"Starting OCR for {file_path}")
        result = ocr.ocr(file_path, cls=True)
        
        full_text = ""
        if result and result[0]:
            # result structure: [[[[x1,y1],[x2,y2],...], ("text", confidence)], ...]
            for line in result[0]:
                text = line[1][0]
                full_text += text + "\n"
        
        logger.info("OCR completed successfully")
        return full_text
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        return ""
