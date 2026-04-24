import PyPDF2

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


def detect_fake_resume(text):
    red_flags = [
        "expert in everything",
        "guaranteed results",
        "100% success",
        "worked in all technologies",
        "10 years experience"
    ]

    found_flags = [flag for flag in red_flags if flag in text.lower()]

    if found_flags:
        return "⚠ Suspicious Resume", found_flags
    else:
        return "✅ Looks Genuine", []