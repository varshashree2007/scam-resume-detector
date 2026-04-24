import streamlit as st
import pickle
import pdfplumber
from resume_detector import analyze_resume

# Load ML model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Page config
st.set_page_config(page_title="AI Detector", layout="wide")

# ---------------- FINAL UI TITLE ----------------
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>
🛡 AI Scam & Resume Detector
</h1>
""", unsafe_allow_html=True)

# ---------------- CSS ----------------
st.markdown("""
<style>
.big-title {
    font-size: 32px;
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

# ---------------- SIDEBAR ----------------
st.sidebar.title("🛡 AI Detector")
page = st.sidebar.radio("Navigate", ["Home", "Scam Detector", "Resume Analyzer", "About"])

st.markdown("---")

# ---------------- HOME ----------------
if page == "Home":
    st.markdown('<div class="big-title">Welcome</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 🚀 Protect Yourself Online
    
    - 📩 Detect scam messages instantly  
    - 📄 Analyze resumes intelligently  
    - 🤖 Powered by Machine Learning  
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📩 Scam Detection")
        st.write("Identify spam messages using ML model")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📄 Resume Analysis")
        st.write("Evaluate resumes with scoring system")
        st.markdown('</div>', unsafe_allow_html=True)

    st.success("👉 Use the sidebar to start")

# ---------------- SCAM DETECTOR ----------------
elif page == "Scam Detector":
    st.markdown('<div class="big-title">📩 Scam Message Detection</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    message = st.text_area("Enter your message")

    if st.button("Analyze Message"):
        if message:
            data = vectorizer.transform([message])
            prediction = model.predict(data)[0]
            prob = model.predict_proba(data)[0]

            confidence = int(max(prob) * 100)

            if prediction == 1:
                st.error("🚨 Spam Message Detected")
                st.progress(confidence)
                st.caption(f"Confidence Score: {confidence}%")
            else:
                st.success("✅ Safe Message")
                st.progress(confidence)
                st.caption(f"Confidence Score: {confidence}%")
        else:
            st.warning("Please enter a message")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RESUME ANALYZER ----------------
elif page == "Resume Analyzer":
    st.markdown('<div class="big-title">📄 Resume Analyzer</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

    if uploaded_file:
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text()

        result, score, flags = analyze_resume(text)

        st.subheader(f"Result: {result}")
        st.write(f"📊 Score: {score}")

        if flags:
            st.warning("⚠ Issues Found:")
            for f in flags:
                st.write("•", f)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ABOUT ----------------
elif page == "About":
    st.markdown('<div class="big-title">ℹ About Project</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 👩‍💻 AI-Based Detection System
    
    This project uses Machine Learning to:
    - Detect scam messages  
    - Analyze resumes with scoring logic  
    
    ### 🛠 Tech Stack
    - Python  
    - Scikit-learn  
    - Streamlit  
    - NLP  
    """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("👩‍💻 Built by Varsha Shree | AI Project 🚀")