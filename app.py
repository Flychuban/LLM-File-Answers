import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from io import StringIO
from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain



def get_raw_text_pdf(uploaded_files):
    read_text = ""
    for uploaded_file in uploaded_files:
        if uploaded_file.name[-4:] == ".pdf":
            print("In pdf reader")
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                read_text += page.extract_text()

        # elif uploaded_file.name[-4:] == ".txt" or uploaded_file.name[-5:] == ".docx":
        #     print("In txt reader: ", uploaded_file.name)
        #     # To convert to a string based IO:
        #     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        #     # To read file as string:
        #     string_data = stringio.read()
        #     read_text += string_data
            
        # elif uploaded_file.name[-4:] == ".csv":
        #     print("In csv reader")
        #     df = pd.read_csv(uploaded_file)
        #     read_text += df.to_string()
        
        # elif uploaded_file.name[-5:] == ".xlsx":
        #     print("In xlsx reader")
        #     df = pd.read_excel(uploaded_file)
        #     # df = df.columns.values
        #     print(df)
        #     read_text += df
            
        
    return read_text

    
def get_conversation(vectorestore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="conversation_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain(
        llm = llm, 
        memory = memory, 
        retriever = vectorestore.as_retriever()
)
    


def main():
    load_dotenv()
    
    st.set_page_config(page_title="LLM File Answers", page_icon=":tyres:")
    st.header("AI Question Answering App based on documents :books:")
    st.text_input("Ask a question about your documents")
    
    with st.sidebar:
        st.subheader("Upload your files for question answering")
        uploaded_files = st.file_uploader("Upload your files and click 'Process'", type=["pdf", "txt", "csv", "xlsx", "docx"], accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing your files..."):
                # Get all the text from the uploaded files
                files_text = get_raw_text_pdf(uploaded_files)
                print(files_text)

                vectorstore = 30 # to be implemented
                
                st.session_state.conversation = get_conversation(vectorestore)

if __name__ == "__main__":
    main() 