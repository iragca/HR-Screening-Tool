import streamlit as st
import pandas as pd
from io import StringIO
import os
from dotenv import load_dotenv
import PyPDF2

#Langchain

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import PyPDFLoader


def file_uploader():

    # FIXME: Duplicate documents can be uploaded
    uploaded_files = st.sidebar.file_uploader(
        "Upload resumes for screening (PDF)", 
        accept_multiple_files=True, 
        type=['pdf']
        )
    splits = []

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=300, 
        chunk_overlap=50
        )

    for uploaded_file in uploaded_files:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        doc = Document(
            page_content=text, 
            metadata={"source": uploaded_file.name}
            )

        splits.append(doc)


    split_docs = text_splitter.split_documents(splits)

    return split_docs if len(split_docs) > 0 else None
