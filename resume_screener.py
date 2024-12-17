from helpers import *

# uuid generator
from uuid import uuid4

load_dotenv()

def ResumeScreener():

    st.session_state.CURRENT_PAGE = st.session_state.RESUME_SCREENER_PAGE

    class EmptyText(Exception):
        """
        A custom exception for when an input component
        like st.text_area is empty.
        """

        def __init__(self, message = 'Text area cannot be empty'):
            self.message = message
            super().__init__(self.message)

    st.set_page_config(
        page_title="Screening Tool",
        page_icon="🔎",
        layout="wide",
        initial_sidebar_state="auto"
    )

    try:
        # raises an error if keys are missing
        check_missing_keys()
        
        # Initialize the vector store -> the pinecone vector store
        vector_store = pinecone_vector_store(
            embedding="text-embedding-3-small",
            index='resumedb'
            ) 

        # File Uploader component -> list of Documents()
        documents = file_uploader() 

        # 'Upload the documents' button to the vector store
        upload_button(
            documents=documents, 
            vector_store=vector_store
            )

        col1, col2 = st.columns(
            spec=[2, 3],
            gap="medium"
            )


        # Job Description text area
        with col1:

            # Dynamic text area height
            st.markdown("""
            <style>
            textarea {
                height: calc(100vh - 350px) !important; /* Adjust based on screen height */
                min-height: 200px; /* Optional: Set a minimum height */
            }
            </style>
            """, unsafe_allow_html=True)

            txt = st.text_area(
            "Describe the job description to match.",
            placeholder = "Position: Data Scientist ...",
            height = 600,
            )

            # Documents to retrieve
            docs_num = st.number_input(
                label="Number of resumes to retrieve",
                step=1,
                min_value=1,
                max_value=100,
                value=10
                )

            if 'DISPLAY_RESULTS' not in st.session_state:
                st.session_state.DISPLAY_RESULTS = False

            # Match resumes button
            if st.button(
                label= 'Match resumes', 
                disabled = st.session_state.KEYS_ARE_MISSING,
                use_container_width = True,
                type = 'primary'
                ):
            
                st.session_state.DISPLAY_RESULTS = True

        # Display the results here
        with col2:
            if st.session_state.DISPLAY_RESULTS:

                # Dynamic UI height
                st.markdown("""
                <style>
                textarea {
                    height: calc(100vh - 350px) !important; /* Adjust based on screen height */
                    min-height: 200px; /* Optional: Set a minimum height */
                }
                </style>
                """, unsafe_allow_html=True)
                with st.container(
                        height=700,
                        border=False
                        ):

                    # The results component
                    match_resumes(
                        job_description=txt,
                        k=docs_num,
                        vector_store=vector_store,
                        summarization_chain=summarize_chain()
                    )

                # Download all as ZIP
                if st.session_state.VECTOR_SCORE:
                    files = pdfs_dict(st.session_state.VECTOR_SCORE)
                    zip_buffer = create_zip_with_pdfs(files, create_pdf)

                    st.download_button(
                        label="Download all as ZIP",
                        data=zip_buffer,
                        file_name=f"resumes-{uuid4()}.zip",
                        mime="application/zip"
                    )

                    st.session_state.DISPLAY_RESULTS = False

    except Exception as e:
        st.error(f"An error in function ResumeScreener has occurred: {e}")