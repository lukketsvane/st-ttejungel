import streamlit as st

def sidebar(on_send_inn_callback):
    st.sidebar.title("Støtte Jungel")
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            "## Slik bruker du tjenesten\n"
            "1. Skriv inn din informasjon\n"
            "2. Last opp PDF, docx, eller txt fil📄\n"
            "3. Send inn og få et utkast til søknaden din 💬\n"
        )
        
           # Add a divider
        st.markdown("---")
        
 
    st.sidebar.markdown("### Velg kulturelle støtteordninger")

    schemes = [
        "Kulturfond",
        "Filmfond",
        "Musikkfond",
        "Kunstfond"
    ]
    
    selected_schemes = st.sidebar.multiselect(
        " ",
        schemes
    )
    
    on_send_inn_callback(selected_schemes)

    uploaded_files = st.sidebar.file_uploader(
        "",
        type=["pdf", "zip", "txt"],
        accept_multiple_files=True,
        help="",
        key="sidebar_file_uploader"  # unique key
    )
    
    return uploaded_files  # Return uploaded_files