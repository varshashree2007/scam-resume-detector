import streamlit as st
import pickle
import numpy as np
from resume_detector import analyze_resume

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Page config
st.set_page_config(page_title="AI Detector", layout="wide")

# Sidebar Navigation
st.sidebar.title("🛡 AI Detector")
page = st.sidebar.radio("Go to", ["🏠 Home", "📩 Scam Detector", "📄 Resume Analyzer", "ℹ About"])

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.title("🛡 AI Scam & Resume Detector")
    st.markdown("""
    ### 🚀 Welcome!
    This application helps you:
    
    ✅ Detect scam messages  
    ✅ Analyze resumes for suspicious content  
    
    Built using Machine Learning + Streamlit
    """)

# ---------------- SCAM DETECTOR ----------------
elif page == "📩 Scam Detector":
    st.title("📩 Scam Message Detection")

    message = st.text_area("Enter your message")

    if st.button("Predict"):
        if message:
            data = vectorizer.transform([message])
            prediction = model.predict(data)[0]
            prob = model.predict_proba(data)[0]

            if prediction == 1:
                st.error(f"🚨 Spam Detected! (Confidence: {max(prob)*100:.2f}%)")
            else:
                st.success(f"✅ Safe Message (Confidence: {max(prob)*100:.2f}%)")
        else:
            st.warning("Please enter a message")

# ---------------- RESUME ANALYZER ----------------
elif page == "📄 Resume Analyzer":
    st.title("📄 Resume Analyzer")

    uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

    if uploaded_file:
        import pdfplumber
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()

        result, flags = analyze_resume(text)

        if "Suspicious" in result:
            st.error(result)
            st.write("⚠ Issues found:")
            for f in flags:
                st.write("- ", f)
        else:
            st.success(result)

# ---------------- ABOUT ----------------
elif page == "ℹ About":
    st.title("ℹ About Project")
    st.markdown("""
    ### 👩‍💻 Project Details
    
    This project detects:
    - Scam messages using ML model
    - Fake or suspicious resumes using keyword analysis
    
    ### 🛠 Tech Used
    - Python
    - Scikit-learn
    - Streamlit
    
    ### 🎯 Purpose
    To improve awareness about online scams and fake resumes.
    """)