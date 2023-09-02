import os
from dotenv import load_dotenv
import streamlit as st
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from knowledge_gpt.components.sidebar import sidebar
from knowledge_gpt.ui import (
    wrap_doc_in_html,
    is_query_valid,
    is_file_valid,
    is_open_ai_key_valid,
    display_file_read_error,
)
from knowledge_gpt.core.caching import bootstrap_caching
from knowledge_gpt.core.parsing import read_file, File
from knowledge_gpt.core.chunking import chunk_file
from knowledge_gpt.core.embedding import embed_files
from knowledge_gpt.core.qa import query_folder

class CombinedFile(File):
    @classmethod
    def from_bytes(cls, file):
        pass

load_dotenv()
EMBEDDING = "openai"
VECTOR_STORE = "faiss"
MODEL = "openai"

def on_send_inn(selected_schemes):
    print("Selected cultural support schemes:", selected_schemes)

st.set_page_config(page_title="StøtteJungelen", page_icon="📖", layout="wide")

css = '''
<style>
    [data-testid='stFileUploader'] button {
        font-size: 0 !important;
    }
    [data-testid='stFileUploader'] button:after {
        content: "Last opp filer";
        font-size: medium !important;
    }
    [data-testid='stFileUploader'] div:last-child {
        font-size: 0 !important;
    }
    [data-testid='stFileUploader'] div:last-child:after {
        content: "Dra og slipp filer her"
        font-size: small !important;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

if 'show_contact_info' not in st.session_state:
    st.session_state['show_contact_info'] = False

bootstrap_caching()

if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []

uploaded_files = sidebar(on_send_inn)
openai_api_key = os.environ.get("OPENAI_API_KEY")

with st.form(key="qa_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        nested_col1, nested_col2 = st.columns([1, 1])
        with nested_col1:
            fornavn = st.text_input("Fornavn", "Steinar")
        with nested_col2:
            etternavn = st.text_input("Etternavn", "Raknes")
        adresse = st.text_input("Adresse", "Bestumveien 5b")
        nested_col3, nested_col4 = st.columns([1, 1])
        with nested_col3:
            postnummer = st.text_input("Postnummer", "0281")
        with nested_col4:
            poststed = st.text_input("Poststed", "Oslo")
    
    with col2:
        prosjekttype = st.selectbox("prosjekttype", ["Musikk", "Annet"])
        
    query = st.text_area("Beskriv prosjektet ditt.")
    submit = st.form_submit_button("Send inn", disabled=(uploaded_files is None or len(uploaded_files) == 0))

if submit:
    st.markdown(f"### Kontaktinformasjon:")
    st.markdown(f"- **Søker/tilskuddsmottaker:** {fornavn}")
    st.markdown(f"- **Fornavn:** {fornavn}")
    st.markdown(f"- **Etternavn:** {etternavn}")
    st.markdown(f"- **Adresse:** {adresse}")
    st.markdown(f"- **Postnummer:** {postnummer}")
    st.markdown(f"- **Poststed:** {poststed}")

combined_docs = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            file = read_file(uploaded_file)
        except Exception as e:
            display_file_read_error(e)
        if not is_file_valid(file):
            st.stop()
        combined_docs.extend(file.docs)

    combined_file = CombinedFile(name="combined", id="combined_id", docs=combined_docs)
    chunked_file = chunk_file(combined_file, chunk_size=300, chunk_overlap=0)

    with st.spinner("Indekserer dokumenter... Dette kan ta litt tid⏳"):
        folder_index = embed_files(
            files=[chunked_file],
            embedding=EMBEDDING,
            vector_store=VECTOR_STORE,
            openai_api_key=openai_api_key,
        )

if submit:
    if not is_query_valid(query):
        st.stop()

    answer_col, sources_col = st.columns(2)

    result = query_folder(
        folder_index=folder_index,
        query=query,
        model=MODEL,
        openai_api_key=openai_api_key,
        temperature=0,
    )

    with answer_col:
        st.markdown("#### Utkast")
        st.markdown(result.answer)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, result.answer)
        pdf_output = io.BytesIO()
        pdf.output(pdf_output)

        st.download_button(
            label="Last ned PDF",
            data=pdf_output.getvalue(),
            file_name="resultat.pdf",
            mime="application/pdf",
        )
