import streamlit as st
import pickle
import PyPDF2

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

st.set_page_config(page_title="AI Detector", layout="wide")

# ---------------- SIDEBAR NAVIGATION ----------------
st.sidebar.title("🛡️ AI Detector")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📩 Scam Detector", "📄 Resume Analyzer", "ℹ️ About"]
)

st.sidebar.markdown("---")
st.sidebar.write("Built using Machine Learning")

# =====================================================
# 🏠 HOME PAGE
# =====================================================
if page == "🏠 Home":
    st.title("🛡️ AI Scam & Resume Detector")

    st.markdown("""
    Welcome to the **AI-based Scam Detection and Resume Analyzer**.

    ### 🔍 Features:
    - Detect scam messages using Machine Learning
    - Analyze resumes and provide score
    - Simple and interactive interface

    ### 🚀 Technologies Used:
    - Python
    - Streamlit
    - Scikit-learn
    """)

# =====================================================
# 📩 SCAM DETECTOR PAGE
# =====================================================
elif page == "📩 Scam Detector":
    st.title("📩 Scam Message Detection")

    msg = st.text_area("Enter your message here")

    if st.button("Predict Scam"):
        if msg.strip():
            vec = vectorizer.transform([msg])

            prediction = model.predict(vec)[0]
            prob = model.predict_proba(vec)[0][prediction]

            if prediction == 1:
                st.error(f"⚠️ Scam Message Detected ({prob*100:.2f}% confidence)")
            else:
                st.success(f"✅ Safe Message ({prob*100:.2f}% confidence)")
        else:
            st.warning("Please enter a message")

# =====================================================
# 📄 RESUME ANALYZER PAGE
# =====================================================
elif page == "📄 Resume Analyzer":
    st.title("📄 Resume Analyzer")

    file = st.file_uploader("Upload Resume (PDF only)")

    def resume_score(text):
        score = 0

        skills = [
            "python", "java", "c++", "sql",
            "machine learning", "data science",
            "flask", "streamlit", "html", "css"
        ]

        text_lower = text.lower()

        for skill in skills:
            if skill in text_lower:
                score += 10

        if "experience" in text_lower:
            score += 10

        if "education" in text_lower or "college" in text_lower:
            score += 10

        return min(score, 100)

    if file is not None:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page_pdf in reader.pages:
            text += page_pdf.extract_text() or ""

        st.subheader("📄 Resume Preview")
        st.write(text[:800])

        if st.button("Analyze Resume"):
            score = resume_score(text)

            st.subheader(f"📊 Resume Score: {score}/100")

            if score > 70:
                st.success("✅ Strong Resume")
            elif score > 40:
                st.warning("⚠️ Average Resume")
            else:
                st.error("❌ Weak Resume")

            st.info("💡 Tip: Add skills, projects, and experience to improve score")

# =====================================================
# ℹ️ ABOUT PAGE
# =====================================================
elif page == "ℹ️ About":
    st.title("ℹ️ About This Project")

    st.markdown("""
    This project is an **AI-based web application** developed using **Machine Learning and Streamlit**.

    ### 🎯 Objective:
    - Detect scam messages using NLP techniques
    - Analyze resumes and provide feedback

    ### 🧠 Model Used:
    - TF-IDF Vectorizer
    - Logistic Regression

    ### 👩‍💻 Developed By:
    - Your Name

    ### 📌 Use Cases:
    - Cyber safety awareness
    - Resume screening
    """)