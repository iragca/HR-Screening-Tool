from helpers import *

def UserDocumentation():

    st.session_state.CURRENT_PAGE = st.session_state.USER_DOC_PAGE

    st.set_page_config(
        page_title="User Documentation", 
        page_icon="🧾"
        )


    st.html('<a name="description"></a>')
    st.markdown("""
    # Description

    The HR Resume Screening Assistance Tool is designed to streamline and 
    optimize the candidate selection process for HR professionals.
    It utilizes artificial intelligence to match job descriptions with 
    potential candidates' resumes, ensuring accuracy and efficiency. With 
    this tool, users can input job descriptions, upload resumes in PDF 
    format, and view top matching resumes or candidates. The goal is to 
    enhance recruitment by saving time and delivering data-driven results. 
    
    This tool is ideal for HR managers, recruiters, and staffing agencies. 
    It operates on standard modern web browsers without requiring 
    installation. Key features include job description input, resume 
    upload functionality, and top match analysis. Users can maximize its 
    potential by ensuring resumes are in PDF format for best compatibility.
    """)

    st.html('<a name="features-and-functionality"></a>')
    st.markdown("""
    # Features and Functionality

    The HR Resume Screening Assistance Tool provides four features:

    - **Job Description Input**: Allows HR professionals to input detailed job information, including the title and description, which acts as the foundation for resume matching. It ensures the job criteria are specific and relevant, improving the precision of candidate selection. Users can conveniently enter information through a structured form that supports various job details. This feature is critical for tailoring the tool's output to organizational needs.

    - **Resume Upload**: Supports the uploading of multiple resumes in PDF format for analysis. It ensures compatibility with most standard resume file types while maintaining data integrity during processing. Users can quickly upload files in bulk, saving time and effort. This functionality makes the tool user-friendly and suitable for handling a large volume of candidate resumes.

    - **Top Matches**: Identifies the most relevant resumes by analyzing their similarity to the job description. It ranks candidates based on their match scores, helping HR professionals prioritize suitable applicants. This feature eliminates manual sorting and enhances decision-making by providing a curated list of candidates. It enables efficient shortlisting for further recruitment steps.
    """)


    st.html('<a name="usage"></a>')
    st.markdown("""
    # Usage
    """)

    st.html('<a name="getting-started"></a>')
    st.markdown("""
    ## Getting Started

    1. Access the Tool: Open the tool in a web browser by entering the provided URL or accessing it through the organization’s HR portal.

    2. Set Up: No installation is required. Ensure you have a stable internet connection and the latest version of a supported browser (e.g., Chrome, Firefox, or Edge).

    3. Input Job Description: Use the "Input Job Description" section to enter the job title and a detailed description of the position.

    4. Upload Resumes: Navigate to the "Upload Resumes" section and upload PDF files of candidates' resumes. You can upload multiple resumes at once.

    5. Generate Matches: Click "Generate" to process the resumes and find the top matches.

    6. Explore Results: Review the top matches, including their summaries and matching scores.
    """)

    st.html('<a name="step-by-step-instructions"></a>')
    st.markdown("""
    ## Step-by-Step Instructions
    How to Use the Tool:

    1. **Open the tool** in your browser.
    2. In the **"Input Job Description"** section:
        - Enter the job title.
        - Provide a detailed job description.
        - Click Submit.
    3. Scroll to the **"Upload Resumes"** section:
        - Click Upload and select PDF resumes from your computer.
        - Ensure all necessary resumes are uploaded.
    4. Click the **Generate** button to start the analysis.
    5. Navigate to the **"Top Matches"** section:
        - Review the list of candidates.
        - Explore each candidate’s summary and match score.
    6. Use the matching scores to shortlist candidates for further evaluation.
    """)


    def _display_faq(question: str, answer: str):
        """
        Display a FAQ question and answer within a sidebar expander.

        Params:
            question (str): The question to display.
            answer (str): The answer to the question.
        """
        with st.expander(question):
            st.write(answer)


    st.html('<a name="troubleshooting-and-faq"></a>')
    st.markdown("""
    # Troubleshooting and FAQ
    """)

    _display_faq(
        question = "What file format does the tool support for resumes?",
        answer = "The tool only accepts resumes in PDF format. Ensure all files are converted to PDF before uploading."
    )

    _display_faq(
        question = """Why is the "Generate" button not working?""",
        answer = """Ensure that both the job description and at least one resume are uploaded before clicking "Generate"."""
    )

    _display_faq(
        question = "What if a resume upload fails?",
        answer = "Check if the file size exceeds the maximum limit or if the file is in a supported format (PDF)."
    )




    st.sidebar.markdown("""
    [Description](#description)

    [Features and Functionality](#features-and-functionality)

    [Usage](#usage)

    [Getting Started](#getting-started)
    
    [Step-by-step Instructions](#step-by-step-instructions)

    [Troubleshooting and FAQ](#troubleshooting-and-faq)
    """)
