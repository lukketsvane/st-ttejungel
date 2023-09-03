import streamlit as st

def sidebar(on_send_inn_callback):
    st.sidebar.title("StøtteJungelen")

    st.sidebar.markdown(
        "1. Skriv inn din informasjon\n"
        "2. Last opp PDF, docx, eller txt fil📄\n"
        "3. Send inn og få et utkast til søknaden din 💬\n"
    )

    uploaded_files = st.sidebar.file_uploader(
        "Drag and Drop",
        type=["pdf", "zip", "txt"],
        accept_multiple_files=True,
        help="",
        key="sidebar_file_uploader"
    )

    schemes = [
        'Fond for lyd og bilde',
        'Drammen Kommunes Kunstnerstipend',
        'Stipend til Internasjonal Kunstnerutveksling'
    ]
    selected_schemes = st.sidebar.selectbox("Velg støtteordning", schemes)
    
    with st.sidebar.form(key='send_inn_form'):
        submit = st.form_submit_button('Send inn')

    on_send_inn_callback(selected_schemes)
    
    return uploaded_files, selected_schemes, submit
