import streamlit as st
import pandas as pd

from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.agents import create_csv_agent

from htmlTemplates import *

def get_file_text(uploaded_files):
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
            
        elif uploaded_file.name[-4:] == ".csv":  # Handle CSV files
            print("In csv reader")
            df = pd.read_csv(uploaded_file)
            print(df)

            read_text += df.to_string()
        
        elif uploaded_file.name[-5:] == ".xlsx":
            print("In xlsx reader")
            df = pd.read_excel(uploaded_file)
            # df = df.columns.values
            print(df)
            
            read_text += df.to_string(index=False)  # You can adjust this as needed
            
            
    return read_text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")

    user_question = st.text_input("Ask a question about your documents:")

    st.button("Ask")

    if user_question or (user_question and st.button("Ask")):
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        files = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if files:
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_file_text(files)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()