import PyPDF2

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


def analyze_resume(text):
    red_flags = [
        "expert in everything",
        "guaranteed results",
        "100% success",
        "worked in all technologies",
        "10 years experience"
    ]

    flags = []

    for phrase in red_flags:
        if phrase.lower() in text.lower():
            flags.append(f"Suspicious phrase found: {phrase}")

    if len(text) < 100:
        flags.append("Resume content is too short")

    if flags:
        return "⚠ Suspicious Resume", flags
    else:
        return "✅ Genuine Resume", []
    