import streamlit as st
import requests

st.title("📄 Plagiarism Checker (Flask + Streamlit)")

original_file = st.file_uploader("Upload Original File", type=["txt"])
submission_file = st.file_uploader("Upload Submission File", type=["txt"])

if st.button("Check Plagiarism") and original_file and submission_file:
    with st.spinner("Processing..."):
        files = {
            "original": original_file,
            "submission": submission_file
        }
        response = requests.post("http://localhost:5000/check", files=files)

        if response.status_code == 200:
            data = response.json()

            st.metric("Similarity Score", f"{data['similarity_score']*100:.2f}%")
            st.metric("Plagiarism Probability", f"{data['probability']*100:.2f}%")

            if data["plagiarized"]:
                st.error("🚨 Plagiarism Detected!")
            else:
                st.success("✔ No Plagiarism Found!")

            st.markdown("### 🔍 Highlighted Original Text")
            st.markdown(data["highlighted_original"], unsafe_allow_html=True)

            st.markdown("### 🔍 Highlighted Submission Text")
            st.markdown(data["highlighted_submission"], unsafe_allow_html=True)
        else:
            st.error("API Error")
