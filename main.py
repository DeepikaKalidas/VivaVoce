import streamlit as st
import os
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
st.write("testing connection to Gemini API")

if st.button("Test gemini API"):
    try:
        response=client.models.generate_content(
            model="gemini-3.8-flash",
            contents="Hello my mini helper!"
        )
        st.success("YAY successful")
        st.write(response.text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")