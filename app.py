import streamlit as st
import pickle
from resume_detector import analyze_resume
import pdfplumber

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Page config
st.set_page_config(page_title="AI Detector", layout="wide")

# Custom CSS
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.big-title {
    font-size: 42px;
    font-weight: bold;
    color: #4CAF50;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #1c1f26;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🛡 AI Detector")
page = st.sidebar.radio("Navigate", ["Home", "Scam Detector", "Resume Analyzer", "About"])

# ---------------- HOME ----------------
if page == "Home":
    st.markdown('<div class="big-title">🛡 AI Scam & Resume Detector</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 🚀 Protect Yourself Online
    
    This AI-powered tool helps you:
    
    - 📩 Detect scam messages instantly  
    - 📄 Analyze resumes for suspicious content  
    - 🤖 Use machine learning for safety
    
    ---
    """)

    st.success("👉 Use the sidebar to explore features")

# ---------------- SCAM DETECTOR ----------------
elif page == "Scam Detector":
    st.markdown('<div class="big-title">📩 Scam Message Detection</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        message = st.text_area("Enter your message")

        if st.button("Analyze Message"):
            if message:
                data = vectorizer.transform([message])
                prediction = model.predict(data)[0]
                prob = model.predict_proba(data)[0]

                confidence = int(max(prob) * 100)

                if prediction == 1:
                    st.error("🚨 Spam Detected!")
                    st.progress(confidence)
                    st.write(f"Confidence: {confidence}%")
                else:
                    st.success("✅ Safe Message")
                    st.progress(confidence)
                    st.write(f"Confidence: {confidence}%")
            else:
                st.warning("Please enter a message")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RESUME ANALYZER ----------------
elif page == "Resume Analyzer":
    st.markdown('<div class="big-title">📄 Resume Analyzer</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

        if uploaded_file:
            text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()

            result, flags = analyze_resume(text)

            if "Suspicious" in result:
                st.error(result)
                for f in flags:
                    st.write("⚠", f)
            else:
                st.success(result)

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ABOUT ----------------
elif page == "About":
    st.markdown('<div class="big-title">ℹ About</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 👩‍💻 Project Info
    
    This project uses Machine Learning to:
    - Detect scam messages
    - Identify suspicious resumes
    
    ### 🛠 Tech Stack
    - Python
    - Scikit-learn
    - Streamlit
    
    ---
    """)
    
# Footer
st.markdown("---")
st.markdown("👩‍💻 Built by Varsha Shree | AI Project 🚀")