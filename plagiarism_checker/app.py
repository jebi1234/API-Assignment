import streamlit as st
import joblib
from utils import calculate_cosine_similarity, highlight_matching_text

model = joblib.load("plagiarism_model.pkl")

st.title("📄 Plagiarism Checker")

file1 = st.file_uploader("Upload Original File", type=["txt"])
file2 = st.file_uploader("Upload Submission File", type=["txt"])

if file1 and file2:
    text1 = file1.read().decode("utf-8")
    text2 = file2.read().decode("utf-8")

    similarity = calculate_cosine_similarity(text1, text2)
    prediction = model.predict([[similarity]])[0]
    prob = model.predict_proba([[similarity]])[0][1]

    st.markdown(f"### 🔢 Cosine Similarity: `{similarity:.2f}`")
    st.markdown(f"### 🎯 Plagiarism Probability: `{prob:.2f}`")

    if prediction == 1:
        st.error("🚨 Plagiarism Detected!")
    else:
        st.success("✔ No Plagiarism Found")

    st.subheader("📌 Highlighted Matching Text")
    h1, h2 = highlight_matching_text(text1, text2)

    st.markdown("#### Original File")
    st.markdown(h1, unsafe_allow_html=True)

    st.markdown("#### Submission File")
    st.markdown(h2, unsafe_allow_html=True)
