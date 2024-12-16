<h1 align="center">HR Screening Tool</h1>

## Installation

Installation can be done locally or have an instance hosted in your own [HuggingFace space](https://huggingface.co/spaces).

### Local installation

Requirements: Python, Streamlit

1. Download this repository as ZIP
2. Extract the ZIP into a folder.
3. Open your terminal and run the following command with the working directory as the extract folder.

```bash
pip install -r requirements.txt
```
4. Wait for the installation of dependencies to complete.
5. Make an `.env` file and write the corresponding needed API keys. Replace the placeholders `<key>` (inclusive). For example:

```env
OPENAI_API_KEY = <OpenAI API key>
PINECONE_API_KEY = <Pinecone API key>
```
6. Run the application using the following command
```bash
streamlit run app.py
```

### HuggingFace

Requirements: HuggingFace account (Free Tier)

You can either use my space as is and just skip to **Step 2**.

1. Clone my repository

![](https://github.com/iragca/HR-Screening-Tool/blob/main/docs/brave_vU07N8VQ11.png?raw=true)


2. Set your API keys by navigating to Settings > Variable and Secrets

![](https://github.com/iragca/HR-Screening-Tool/blob/main/docs/brave_6lBnGhWTE4.png?raw=true)

![](https://github.com/iragca/HR-Screening-Tool/blob/main/docs/brave_jKUWhHLjcF.png?raw=true)

3. Set your API keys ('OPENAI_API_KEY', 'PINECONE_API_KEY') with their value by replacing the `<placeholder>' (inclusive.)

![](https://github.com/iragca/HR-Screening-Tool/blob/main/docs/brave_nBeqDrwLnQ.png?raw=true)

4. You can now start the using the app by clicking on the 'App' button on the main repository page.

![](https://github.com/iragca/HR-Screening-Tool/blob/main/docs/brave_d30L5ZBh04.png?raw=true)
