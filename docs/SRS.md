# Software Requirements Specification (SRS)

## 1. [Introduction](#introduction)
### 1.1 [Purpose](#purpose)
The purpose of this document is to define the functional and non-functional requirements for a Generative AI HR Screening Software tool. This tool will streamline the resume screening process by using AI to match resumes with job descriptions, ensuring HR employees can identify the best candidates efficiently.

### 1.2 [Scope](#scope)
The software will allow HR employees to upload multiple resumes in PDF format and input a job description. Using AI models and vector search, the tool will identify and rank the resumes that most closely match the provided job description. The system will leverage Python, Streamlit, OpenAI models, and the Pinecone vector database to deliver a user-friendly experience with high precision and responsiveness.

### 1.3 [Users and Use Case](#users-and-use-case)
- **Primary Users:** HR employees.
- **Use Case:** HR employees upload resumes and a job description, and the software outputs the top matching resumes ranked by relevance.

## 2. [Functional Requirements](#functional-requirements)
### 2.1 [Input Requirements](#input-requirements)
- The system must accept multiple resumes in PDF format.
- The system must accept a job description as plain text or a PDF.

### 2.2 [Processing Requirements](#processing-requirements)
- The system must parse the resumes and job description into textual data.
- The system must encode the textual data using embeddings via OpenAI models.
- The system must store and query embeddings using Pinecone's vector database.
- The system must rank resumes based on their similarity to the job description using cosine similarity or equivalent.

### 2.3 [Output Requirements](#output-requirements)
- The system must display a ranked list of the top-matching resumes.
- Each result must include:
  - Candidate's name (if extracted from the resume).
  - A similarity score.
  - A brief summary of the candidate's relevant skills or experience (if extractable).

### 2.4 [User Interface (UI) Requirements](#user-interface-ui-requirements)
- The UI must allow HR employees to:
  - Upload resumes in bulk (drag-and-drop functionality preferred).
  - Input or upload the job description.
  - View results in an easy-to-read, visually appealing format (e.g., ranked table or cards).
  - Export results as a CSV or PDF.
- The UI must be responsive and intuitive, designed with HR employees in mind.

## 3. [Non-Functional Requirements](#non-functional-requirements)
### 3.1 [Performance](#performance)
- The system must process and rank up to 50 resumes in under 30 seconds.
- The system must handle job descriptions of up to 500 words.

### 3.2 [Scalability](#scalability)
- The system must scale to accommodate 100 concurrent users without performance degradation.

### 3.3 [Usability](#usability)
- The system must provide a minimal learning curve for HR employees.
- The UI must adhere to modern design principles, ensuring aesthetic appeal and ease of use.

### 3.4 [Security](#security)
- Resumes and job descriptions must be encrypted during upload and processing.
- User data must comply with GDPR and other relevant data protection regulations.

### 3.5 [Reliability](#reliability)
- The system must maintain a 99% uptime during business hours (8 AM - 6 PM).

## 4. [System Architecture](#system-architecture)
### 4.1 [Tools and Frameworks](#tools-and-frameworks)
- **Backend:** Python for processing resumes and job descriptions.
- **Frontend:** Streamlit for building an interactive and user-friendly UI.
- **AI Models:** OpenAI for generating embeddings and ranking results.
- **Database:** Pinecone vector database for similarity search and storage.

### 4.2 [Workflow](#workflow)
#### Input Processing:
1. HR employees upload resumes and job descriptions.
2. Resumes are parsed, and embeddings are generated.

#### Storage and Matching:
1. Embeddings are stored in Pinecone and queried using the job description embedding.

#### Output Generation:
1. Top resumes are retrieved, ranked, and displayed to the user.

## 5. [Constraints](#constraints)
- The system must only process resumes and job descriptions in English.
- OpenAI models must be used under their rate limits and API constraints.
- Pinecone's database usage must stay within the allocated quota.

## 6. [Future Enhancements](#future-enhancements)
- Integration with Applicant Tracking Systems (ATS).
- Support for multi-language resumes and job descriptions.
- Additional ranking metrics (e.g., based on specific skills or certifications).
- Custom filters for HR employees (e.g., years of experience, education level).
