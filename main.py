
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from document_parser import extract_text
from database import get_libraries, create_tables, create_library

create_tables()

# Load environment variables
load_dotenv()

# Connect to Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Streamlit page configuration
st.set_page_config(
    page_title="VivaVoce",
    page_icon="🎙️",
    layout="centered"
)


# App heading
st.title("VivaVoce: My mini helper")
st.caption("Your AI-powered active recall assistant")


st.header("My Study Libraries")

# Create a new library
library_name = st.text_input(
    "Name your study library",
    placeholder="e.g. Operating Systems"
)

if st.button("Create Library"):

    if library_name.strip() == "":
        st.warning("Please enter a library name.")

    else:
        created = create_library(library_name.strip())

        if created:
            st.success(f"{library_name} created successfully! 🎉")

        else:
            st.warning("A library with this name already exists.")


# Display existing libraries
st.subheader("Your Libraries")

libraries = get_libraries()

if libraries:

    for library in libraries:
        library_id, name = library

        st.write(f"📚 {name}")

else:
    st.info("You haven't created any libraries yet.")


st.header("Upload your study material")

uploaded_files = st.file_uploader(
    "Upload your study material",
    type=["pdf", "docx", "pptx"],
    accept_multiple_files=True
)


# Process uploaded documents
if uploaded_files:

    if len(uploaded_files) > 15:

        st.error("You can upload a maximum of 15 documents.")

    else:

        st.success(f"{len(uploaded_files)} documents uploaded!")

        documents = {}

        # Extract text from every uploaded document
        for uploaded_file in uploaded_files:

            extracted_text = extract_text(
                uploaded_file.name,
                uploaded_file.getvalue()
            )

            documents[uploaded_file.name] = extracted_text

        st.success("All documents processed!")

        # Display extracted document contents
        for file_name, content in documents.items():

            with st.expander(file_name):

                st.text_area(
                    "Extracted content",
                    content,
                    height=200,
                    key=file_name
                )

        # Combine all documents into one string
        combined_text = "\n\n".join(documents.values())


        # Generate a viva question
        if st.button("Generate my first question"):

            prompt = f"""
You are VivaVoce, an AI-powered active recall assistant.

You are a small but powerful tool that helps students
learn and retain information effectively.

Read the study material below and generate exactly
ONE relevant viva question.

Do not provide the answer.
Only provide the question.

Study material:
{combined_text}
"""

            try:

                st.write("Your mini helper is thinking...")

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

                st.subheader("Your first viva question 🎙️")

                st.write(response.text)

            except Exception as e:

                st.error(f"Something went wrong: {e}")
