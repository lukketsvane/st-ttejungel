import os
from dotenv import load_dotenv
import streamlit as st
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from knowledge_gpt.components.sidebar import sidebar
from knowledge_gpt.core.caching import bootstrap_caching
from knowledge_gpt.core.parsing import read_file, File
from knowledge_gpt.core.chunking import chunk_file
from knowledge_gpt.core.embedding import embed_files
from knowledge_gpt.core.qa import query_folder
from knowledge_gpt.ui import is_file_valid

class CombinedFile(File):
    @classmethod
    def from_bytes(cls, file):
        pass

load_dotenv()
EMBEDDING = "openai"
VECTOR_STORE = "faiss"
MODEL = "openai"

current_directory = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(current_directory, "template-1.txt"), "r", encoding='utf-8') as f:
    template_1 = f.read()

with open(os.path.join(current_directory, "template-2.txt"), "r", encoding='utf-8') as f:
    template_2 = f.read()

with open(os.path.join(current_directory, "template-3.txt"), "r", encoding='utf-8') as f:
    template_3 = f.read()

STOTTEORDNING_TEMPLATES = {
    'Fond for lyd og bilde': template_1,
    'Drammen Kommunes Kunstnerstipend': template_2,
    'Stipend til Internasjonal Kunstnerutveksling': template_3,
}

def on_send_inn(selected_schemes):
    return STOTTEORDNING_TEMPLATES.get(selected_schemes, "No Template")


bootstrap_caching()

st.set_page_config(page_title="StøtteJungelen", page_icon="📖", layout="wide")

css = '''<style>
    .stText, .stMarkdown, .stTextArea {
        padding-left: 10%;
        padding-right: 10%;
    }
</style>'''
st.markdown(css, unsafe_allow_html=True)

openai_api_key = os.environ.get("OPENAI_API_KEY")

uploaded_files, selected_schemes, submit = sidebar(on_send_inn)
selected_templates = on_send_inn(selected_schemes)  # This line selects the template based on the scheme


query = st.text_area("Beskriv prosjektet ditt.")
combined_docs = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        file = read_file(uploaded_file)
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
        query=selected_templates,  # This line uses the selected template
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
