import PyPDF2
import re

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


def analyze_resume(text):
    score = 0
    flags = []

    text_lower = text.lower()

    # 🔹 Skills detection
    skills = ["python", "java", "machine learning", "data analysis", "sql"]
    found_skills = [skill for skill in skills if skill in text_lower]

    if found_skills:
        score += len(found_skills) * 10
    else:
        flags.append("No relevant technical skills found")

    # 🔹 Suspicious phrases
    suspicious = [
        "expert in everything",
        "guaranteed results",
        "100% success",
        "worked in all technologies"
    ]

    for phrase in suspicious:
        if phrase in text_lower:
            flags.append(f"Suspicious claim: {phrase}")
            score -= 15

    # 🔹 Length check
    if len(text) < 300:
        flags.append("Resume content too short")
        score -= 10

    # 🔹 Email check
    if not re.search(r"\S+@\S+\.\S+", text):
        flags.append("Email not found")
        score -= 10
    else:
        score += 10

    # 🔹 Final result
    if score >= 30:
        result = "✅ Strong Resume"
    elif score >= 10:
        result = "⚠ Average Resume"
    else:
        result = "🚨 Weak / Suspicious Resume"

    return result, score, flags