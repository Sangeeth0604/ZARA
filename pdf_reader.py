import os
import PyPDF2
from ai_brain import ask_ai

def find_latest_pdf(folder_path):
    pdf_files = []

    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            pdf_files.append(
                os.path.join(folder_path, file)
            )

    if not pdf_files:
        return None

    return max(pdf_files, key=os.path.getctime)

def read_pdf(pdf_path):
    text = ""

    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                text += page.extract_text() + "\n"

        return text

    except Exception as e:
        return f"PDF Error: {e}"

def summarize_latest_pdf():
    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    pdf_path = find_latest_pdf(desktop)

    if not pdf_path:
        return "No PDF found on Desktop."

    text = read_pdf(pdf_path)

    if len(text) > 6000:
        text = text[:6000]

    prompt = f"""
Summarize this PDF in simple words.

{text}
"""

    return ask_ai(prompt)