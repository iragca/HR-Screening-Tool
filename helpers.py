# Streamlit stuff
import streamlit as st
from streamlit_lottie import st_lottie

# Misc
import pandas as pd
from io import StringIO
import zipfile
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from dotenv import load_dotenv
import PyPDF2
import re

# Type hinting
from typing import List

# Langchain
# from langchain.schema import Document
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Pinecone; from pinecone import Pinecone as PC
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

@st.cache_resource
def summarize_chain():
    """
    Returns a LangChain LLMChain for summarizing resumes.
    """

    resume_summary_prompt = PromptTemplate(
        input_variables=["text"],
        template="""
        You are an AI expert in summarizing resumes. Given the following resume text:

        {text}

        Please provide a concise summary of the candidate's qualifications, experience, and skills in no more than 5 sentences.
        """
    )

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=200)

    summarization_chain = LLMChain(llm=llm, prompt=resume_summary_prompt)

    return summarization_chain



def check_missing_keys():
    """
    Checks if necessary environment variables are set for the application to work.
    Raises a KeyError if any required keys are missing.
    """

    try:

        st.session_state.KEYS_ARE_MISSING = False

        keys = {
            "OpenAI": os.getenv("OPENAI_API_KEY"),
            "Pinecone": os.getenv("PINECONE_API_KEY")
        }
        
        missing_keys = []
        for key, value in keys.items():
            if not value:
                missing_keys.append(key)

        if len(missing_keys) > 0:
            st.session_state.KEYS_ARE_MISSING = True
            raise KeyError(f"Missing required API keys: {', '.join(missing_keys)}")

    except KeyError as e:
        st.error(e)

def file_uploader() -> List[Document]:
    """
    Initializes a file uploader component to the sidebar

    Returns: None or a list of Document() objects
    """

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

def pinecone_vector_store(embedding: str, index: str) -> Pinecone:
    """
    Initializes a Pinecone vector store

    Params:
        embedding (str): The name of the OpenAI model for embedding

    Returns: Pinecone object or None if an error occurs
    """

    try:
        embeddings = OpenAIEmbeddings(
        model=embedding
        )

        vector_store = Pinecone.from_existing_index(
            index_name=index,
            embedding=embeddings
        )

        return vector_store

    except Exception as e:
        st.error(f"Error connecting to Pinecone: {e}")
        return None

def upload_button(documents: List[Document], vector_store: Pinecone):
    """
    Initializes a button to upload files to the vector store

    Params:
        documents (list of Document()): The documents to be uploaded
        vector_store (Pinecone): The vector store to which the documents will be uploaded
    """

    class EmptyUpload(Exception):
        """
        A custom exception for when an an upload component
        is empty.
        """
        def __init__(self, message = 'No files were uploaded'):
            self.message = message
            super().__init__(self.message)
    
    if st.sidebar.button(
        'Store to the Database', 
        key='vector-store', 
        disabled=st.session_state.KEYS_ARE_MISSING
        ):

        try:
            if documents is None:
                raise EmptyUpload

            uuids = [str(uuid4()) for _ in range(len(documents))]
            vector_store.add_documents(documents=documents, ids=uuids)
            
        except EmptyUpload as e:
            st.sidebar.error(f"Error storing documents: {e}")
        except Exception as e:
            st.sidebar.error(f"An error in function upload_button has occurred: {e}")
        else:
            st.sidebar.success('Documents stored successfully!')

@st.fragment
def match_resumes(
    job_description: str, 
    k: int, 
    vector_store: Pinecone, 
    summarization_chain: LLMChain
    ):

    class EmptyText(Exception):
        """
        A custom exception for when an input component
        like st.text_area is empty.
        """
        def __init__(self, message = 'Text area cannot be empty'):
            self.message = message
            super().__init__(self.message)

    class NoResults(Exception):
        """
        A custom exception for when there no results retrieved.
        """
        def __init__(self, message = 'No matched results found'):
            self.message = message
            super().__init__(self.message)

    try:
        with st.status("Fetching matching resumes...") as status:
            if job_description == '':                    
                status.update(
                    label="Failed", 
                    state="error", 
                    expanded=False
                )
                raise EmptyText

            if 'VECTOR_SCORE' not in st.session_state:
                st.session_state.VECTOR_SCORE = None

            st.session_state.VECTOR_SCORE = vector_store.similarity_search_with_relevance_scores(job_description, k=k)
            vector_score = st.session_state.VECTOR_SCORE #variable alias

            if len(vector_score) == 0:
                status.update(
                    label="Failed", 
                    state="error", 
                    expanded=False
                )
                raise NoResults

            status.update(
                label="Found matches...", 
                state="running", 
                expanded=False
            )


            tab1, tab2 = st.tabs(["Summary", "Detailed View"])

            with tab1:
                st.write(f"""
                **Matched resumes:** {len(vector_score)}

                **Highest score:** {round(max([x[1] for x in vector_score]) * 100, 2)}%

                **Lowest score:** {round(min([x[1] for x in vector_score]) * 100, 2)}%
                \n\n\n

                ### **Quick Overview**

                ---
                """)
                status.update(
                    label="Summarizing results...", 
                    state="running", 
                    expanded=False
                )


                for i in range(0, len(vector_score)):
                    doc, score = vector_score[i]
                    resume = re.search(r'([^/]+\.pdf)$', doc.metadata['source'])

                    st.write(f"#### **Match Number:** {i+1}")
                    st.write(f"**Resume:** {resume.group(1)}" + \
                        f"\n\n**Relevance:** {round(float(score) * 100, 2)}%")
                    # st.write(f"**AI Generated Summary:**\n\n{summarization_chain.run(text=doc.page_content)}")
                    st.write(f"**AI Generated Summary:**\n\n{doc.page_content[0:50]}") # debugging and testing purposes
                    st.write("---")

                status.update(
                    label="Done", 
                    state="complete", 
                    expanded=True
                )

            with tab2:
                for i in range(0, len(vector_score)):
                    doc, score = vector_score[i]

                    resume = re.search(r'([^/]+\.pdf)$', doc.metadata['source'])

                    st.write(f"#### **Match Number:** {i+1}")
                    st.write(f"**Resume:** {resume.group(1)}" )
                    st.write(f"**Relevance:** {round(float(score) * 100, 2)}%")
                    st.write(f"**Content:**\n\n{doc.page_content}")
                    st.write("---")

    except EmptyText as e:
        st.error(e)
    except NoResults as e:
        st.error(e)
    except Exception as e:
        st.error(f"An error in function match_resumes has occurred: {e}")

# Function to generate a PDF file
def create_pdf(content):
    try:
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        width, height = letter  # Get page dimensions

        # Define text wrapping parameters
        x_margin = 50  # Left margin
        y_margin = 750  # Starting y-position
        line_height = 15  # Line spacing
        max_width = width - 2 * x_margin  # Text area width

        # Split content into lines that fit within the max_width
        from reportlab.pdfbase.pdfmetrics import stringWidth
        words = content.split()
        current_line = ""
        y_position = y_margin
        for word in words:
            # Check if adding the next word exceeds max_width
            if stringWidth(current_line + " " + word, "Helvetica", 12) <= max_width:
                current_line += " " + word
            else:
                # Draw the current line and reset for the next
                c.drawString(x_margin, y_position, current_line.strip())
                y_position -= line_height  # Move to the next line
                current_line = word
                # Check if we're running out of space on the page
                if y_position < 50:  # Bottom margin
                    c.showPage()  # Start a new page
                    y_position = y_margin  # Reset y-position

        # Draw the last line
        if current_line:
            c.drawString(x_margin, y_position, current_line.strip())

        c.save()
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    except Exception as e:
        st.error(f"Error creating PDF: {e}")
        return None

 # Function to create a zip file with multiple PDFs
def create_zip_with_pdfs(pdf_data, create_pdf):
    try:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_name, content in pdf_data.items():
                # Generate PDF for each file
                pdf_bytes = create_pdf(content)
                # Write the PDF into the zip file
                zf.writestr(file_name + ".pdf", pdf_bytes)
        zip_buffer.seek(0)
        return zip_buffer
    except Exception as e:
        st.error(f"Error creating ZIP: {e}")
        return None

def pdfs_dict(vector_score):
    files = dict()
    for i in range(0, len(vector_score)):
        doc, score = vector_score[i]
        resume = re.search(r'([^/]+\.pdf)$', doc.metadata['source'])
        files[f"{resume.group(1)}"] = doc.page_content

    return files