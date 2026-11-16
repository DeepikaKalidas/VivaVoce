import streamlit as st
import os
import fitz
from dotenv import load_dotenv
from google import genai

load_dotenv()

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="VivaVoce",
    page_icon="🎙️",
    layout="centered"
)

st.title("VivaVoce: My mini helper")
st.caption("Your AI-powered active recall assistant")
st.header("Upload your PDF file")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    pdf = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    extracted_text = ""
    for page in pdf:
        extracted_text += page.get_text()

    st.subheader("Extracted study material")
    st.text_area("PDF Content", extracted_text, height=300)


if st.button("Generate my first question"):
        prompt=f"""
You are VivaVoce, an AI-powered active recall assistant,
You are called a mini helper because you are a small but powerful tool that helps students learn and retain information more effectively.
Read the study material below and generate exactly one question that is relevant to the content.
Do not provide any answers, just the question.
Study material:
{extracted_text}
"""
        try:
            response=client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            st.subheader("First viva question")
            st.write(response.text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
