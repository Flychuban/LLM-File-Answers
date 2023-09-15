import streamlit as st
import pandas as pd
from dotenv import load_dotenv

def main():
    st.set_page_config(page_title="Question Answering App", page_icon=":tyres:")
    st.header("AI Question Answering App based on documents :books:")
    st.text_input("Ask a question about your documents")
    
    with st.sidebar:
        st.subheader("Upload your files for question answering")
        uploaded_files = st.file_uploader("Upload your files and click 'Process'", type=["pdf", "txt", "csv", "xlsx"], accept_multiple_files=True)
        if st.button("Process"):
            pass


if __name__ == "__main__":
    main() 