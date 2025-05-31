"""
Modulo: ocr_module.py
Descrizione: Estrae testo da immagini tramite OCR (Tesseract o alternativa).
"""

try:
    import pytesseract
    from PIL import Image
except ImportError as e:
    raise ImportError("Modulo OCR non installato: usa `pip install pytesseract pillow`")

def extract_text_from_image(image_path: str) -> str:
    """
    Estrae il testo da un'immagine (jpg, png) usando OCR.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='ita')  # o 'eng' se preferisci
        return text.strip()
    except Exception as e:
        return f"[❌ Errore OCR]: {str(e)}"
