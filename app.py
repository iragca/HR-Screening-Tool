from helpers import *

load_dotenv()

st.sidebar.title('HR Resume Screening Assistance Tool')

st.sidebar.write('---')

txt = st.text_area(
    "Describe the Job Description to match.",
    height = 300
)

documents = file_uploader()

documents




st.sidebar.write('---')
