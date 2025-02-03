# Regulatory Compliance Checker for Legal Contracts

This project is a **Streamlit-based web application** designed to assist legal professionals and businesses in analyzing legal contracts for regulatory compliance. It provides functionalities to extract key clauses and generate comprehensive analysis reports, offering insights into contract strengths, weaknesses, legal compliance, and areas for improvement.

## Features

- **File Upload Support:** Upload legal contracts in **PDF**, **DOCX**, or **TXT** formats.
- **Key Clause Extraction:** AI-driven extraction of critical clauses from contracts.
- **Detailed Analysis Report:** Generates an in-depth report evaluating the contract's compliance with legal standards, structure, completeness, and quality.
- **Similarity Matching:** Compares the uploaded contract with stored embeddings to identify similar contracts.
- **User-Friendly Interface:** Easy navigation with tabs for **About**, **Extract Key Clauses**, and **Analysis Report**.

## Tech Stack

- **Python**
- **Streamlit** for UI
- **SentenceTransformers** for text embeddings
- **scipy** for similarity calculations
- **PyPDF2** and **python-docx** for document text extraction
- **Groq API** for advanced AI-driven analysis

## Setup Instructions

**`requirements.txt` should include:**
- streamlit
- sentence-transformers
- scipy
- PyPDF2
- python-docx
- requests

### Set API Key
Replace the placeholder API key in the script with your actual Groq API key:
```python
ANALYSIS_API_KEY = "your_api_key_here"
```

### Run the Application
```bash
streamlit run main.py
```

The app will be available at `http://localhost:8501/` by default.

## Usage

1. **Upload a Contract:**
   - Use the file uploader to upload a PDF, DOCX, or TXT contract.

2. **Navigate Tabs:**
   - **About:** Learn about the tool’s functionality.
   - **Extract Key Clauses:** Automatically extract important clauses from the contract.
   - **Analysis Report:** Generate a detailed analysis report, including compliance checks and improvement suggestions.

3. **View Results:**
   - The extracted key clauses and detailed analysis report will be displayed in a clean, formatted interface.

## API Information

The application uses **Groq's API** for contract analysis. Make sure to:

- Sign up at [Groq](https://groq.com) to get your API key.
- Ensure your API key has the necessary permissions for using the AI models.

## Customization

- **Add New Embeddings:**
  - Update the `embeddings.json` file with new contract embeddings to enhance similarity matching.

- **Modify Analysis Parameters:**
  - Customize the prompts in `analyze_with_groq()` and `get_key_clauses()` functions to tailor the analysis to specific legal requirements.

## Troubleshooting

- **Error Processing File:** Ensure the file format is supported (PDF, DOCX, TXT).
- **Embeddings File Not Found:** Ensure `embeddings.json` exists in the project directory.
- **API Errors:** Double-check your API key and ensure you have access to the Groq API.


## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [Groq API](https://groq.com)
