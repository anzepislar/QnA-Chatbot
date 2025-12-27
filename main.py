import streamlit as st
from brain import upload, ask
import tempfile
from pathlib import Path

def save_tempfile(file):
    # Keep extension so your loaders can pick the right parser (pdf/docx/txt)
    suffix = Path(file.name).suffix if getattr(file, "name", None) else ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.getbuffer())
        return tmp.name

if 'doc_ready' not in st.session_state:
    st.session_state.doc_ready = False
    
if 'doc_path' not in st.session_state:
    st.session_state.doc_path = None

file = st.file_uploader('Upload your file.', type=['pdf', 'docx', 'txt'])

if file:
    if st.button('Process'):
        path = save_tempfile(file)
        st.session_state.doc_path = path
        
        with st.spinner('Indexing...'):
            upload(path)
            
        st.session_state.doc_ready = True
        st.success('Document processed.')
        
if st.session_state.doc_ready:
    
    question = st.text_input('Ask question: ')
    
    if st.button('Ask'):
        if not question:
            st.warning('Enter your question first')
            
        else:
            with st.spinner('Thinking...'):
            
                response = ask(q=question, file_path=st.session_state.doc_path)
        
                st.write(response)
                
else:
    st.info('Upload a file and click "process".')
