
import fitz
from docx import Document
from pptx import Presentation
from io import BytesIO


def extract_text(file_name, file_bytes):

    extension = file_name.lower().split(".")[-1]

    if extension == "pdf":

        pdf = fitz.open(
            stream=file_bytes,
            filetype="pdf"
        )

        text = ""

        for page in pdf:
            text += page.get_text() + "\n"

        pdf.close()

    elif extension == "docx":

        document = Document(BytesIO(file_bytes))

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        for table in document.tables:
            for row in table.rows:
                text += " | ".join(
                    cell.text for cell in row.cells
                ) + "\n"

    elif extension == "pptx":

        presentation = Presentation(BytesIO(file_bytes))

        text = ""

        for slide_number, slide in enumerate(presentation.slides, start=1):

            text += f"\nSlide {slide_number}\n"

            for shape in slide.shapes:

                if shape.has_text_frame:
                    text += shape.text + "\n"

                if shape.has_table:
                    for row in shape.table.rows:
                        text += " | ".join(
                            cell.text for cell in row.cells
                        ) + "\n"

    else:
        raise ValueError("Unsupported file format")

    return text.strip()
