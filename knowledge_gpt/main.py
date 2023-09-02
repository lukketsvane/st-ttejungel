import os
from dotenv import load_dotenv
import streamlit as st
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem

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


current_directory = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(current_directory, "template-1.txt"), "r") as f:
    template_1 = f.read()

with open(os.path.join(current_directory, "template-2.txt"), "r") as f:
    template_2 = f.read()
    
with open(os.path.join(current_directory, "template-3.txt"), "r") as f:
    template_3 = f.read()

STOTTEORDNING_TEMPLATES = {
    'Fond for lyd og bilde': template_1,
    'Drammen Kommunes Kunstnerstipend': template_2,
    'Stipend til Internasjonal Kunstnerutveksling': template_3,
}


class CombinedFile(File):
    @classmethod
    def from_bytes(cls, file):
        pass

load_dotenv()
EMBEDDING = "openai"
VECTOR_STORE = "faiss"
MODEL = "openai"

def on_send_inn(selected_schemes):
    if isinstance(selected_schemes, list):
        selected_templates = [STOTTEORDNING_TEMPLATES.get(scheme, "No Template") for scheme in selected_schemes]
    else:
        selected_templates = STOTTEORDNING_TEMPLATES.get(selected_schemes, "No Template")
    print("Selected cultural support schemes:", selected_schemes)
    print("Selected template(s):", selected_templates)

st.set_page_config(page_title="StøtteJungelen", page_icon="📖", layout="wide")
css = '''<style> /* CSS content here */ </style>'''
st.markdown(css, unsafe_allow_html=True)

bootstrap_caching()

uploaded_files = sidebar(on_send_inn)
openai_api_key = os.environ.get("OPENAI_API_KEY")

with st.form(key="qa_form"):
    col1, col2 = st.columns(2)
    fornavn = col1.text_input("Fornavn", "Ola")
    etternavn = col1.text_input("Etternavn", "Nordmann")
    adresse = col1.text_input("Adresse", "Olaveien 1")
    postnummer = col1.text_input("Postnummer", "0281")
    poststed = col1.text_input("Poststed", "Oslo")
    prosjekttype = col2.selectbox("prosjekttype", ["Musikk", "Annet"])
    selected_schemes = col2.selectbox("Velg støtteordning", list(STOTTEORDNING_TEMPLATES.keys()))
    query = col2.text_area("Beskriv prosjektet ditt.")
    submit = st.form_submit_button("Send inn")

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

    folder_index = embed_files(
        files=[chunked_file],
        embedding=EMBEDDING,
        vector_store=VECTOR_STORE,
        openai_api_key=openai_api_key,
    )

if submit:
    result = query_folder(
        folder_index=folder_index,
        query=query,
        model=MODEL,
        openai_api_key=openai_api_key,
        temperature=0,
    )

    st.markdown("#### Utkast")
    st.markdown(result.answer)

    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='ListBullet', parent=styles['BodyText'], spaceAfter=20, bulletIndent=0, leftIndent=20, bulletText='-'))
    
    flowables = []
    
    for line in result.answer.split('\n'):
        if line.startswith('# '):
            flowables.append(Paragraph(line[2:], styles['Heading1']))
        elif line.startswith('## '):
            flowables.append(Paragraph(line[3:], styles['Heading2']))
        elif line.startswith('### '):
            flowables.append(Paragraph(line[4:], styles['Heading3']))
        elif line.startswith('- '):
            flowables.append(ListFlowable([ListItem(Paragraph(line[2:], styles['ListBullet']))]))
        elif line.startswith('**'):
            flowables.append(Paragraph(f"<strong>{line[2:-2]}</strong>", styles['BodyText']))
        else:
            flowables.append(Paragraph(line, styles['BodyText']))
    
    pdf.build(flowables)
    
    st.download_button(
        label="Last ned PDF",
        data=pdf_buffer.getvalue(),
        file_name="resultat.pdf",
        mime="application/pdf",
    )
