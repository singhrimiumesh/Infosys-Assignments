import streamlit as st
import os
import json
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from PyPDF2 import PdfReader
from docx import Document
import requests

model = SentenceTransformer("all-MiniLM-L6-v2")

EMBEDDINGS_PATH = "./embeddings.json"
ANALYSIS_API_KEY = "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"
ANALYSIS_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    return "".join([page.extract_text() for page in reader.pages])

def extract_text_from_docx(filepath):
    doc = Document(filepath)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def get_key_clauses(text):
    system_prompt = (
    "You are an advanced AI assistant specializing in legal document analysis. Your task is to extract key clauses from the provided legal contract text.\n\n"
    "2. **Output :**\n"
    "List of key clauses"
    
    "### Input Contract Text:\n"
    f"{text}"
)


    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Identify the key clauses in this text."}
    ]
    data = {
        "messages": messages,
        "model": "llama3-8b-8192",
        "temperature": 0.7
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ANALYSIS_API_KEY}"
    }
    response = requests.post(ANALYSIS_API_URL, data=json.dumps(data), headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def load_embeddings(embeddings_path):
    with open(embeddings_path, "r") as f:
        return json.load(f)

def find_top_matches(user_text, embeddings_data, top_n=2):
    user_embedding = model.encode(user_text)
    similarity_scores = []

    for entry in embeddings_data:
        stored_embedding = entry["embedding"]
        score = 1 - cosine(user_embedding, stored_embedding)
        similarity_scores.append({
            "score": score,
            "data": entry["metadata"]
        })

    similarity_scores.sort(key=lambda x: x["score"], reverse=True)

    return similarity_scores[:top_n]

def analyze_with_groq(user_text, top_matches):
    prompt = (
    "You are an advanced AI assistant specializing in legal contract analysis, tasked with evaluating agreements based on key parameters such as compliance, clarity, terms, completeness, and overall quality. Your objective is to deliver an in-depth, structured report that identifies the contract's strengths, weaknesses, and alignment with legal and business standards, while providing actionable recommendations for improvement.\n\n"
    
    "# **Instructions for Contract Analysis:**\n"
    "1. **Legal Compliance:**\n"
    "   - Assess whether the contract adheres to relevant legal standards, regulations, and industry practices (e.g., GDPR, HIPAA, corporate laws, privacy regulations, or sector-specific standards).\n"
    "   - Identify any clauses or language that may create potential legal risks.\n\n"
    
    "2. **Clarity and Structure:**\n"
    "   - Evaluate the contract's readability, organization, and structure.\n"
    "   - Highlight sections that may be confusing, overly complex, or vague.\n\n"
    
    "3. **Completeness and Relevance:**\n"
    "   - Identify whether all critical components (e.g., parties, scope, terms, conditions, dispute resolution, indemnities, etc.) are included and appropriately detailed.\n"
    "   - Highlight any missing or irrelevant elements that could affect the contract's enforceability or practicality.\n\n"
    
    "4. **Scoring System:**\n"
    "   - Assign an **Overall Score** from 1 to 100, following these guidelines:\n"
    "     - **1-35**: The contract fails to meet the necessary requirements and poses significant risks.\n"
    "     - **36-70**: The contract meets basic requirements but requires improvement to be effective and enforceable.\n"
    "     - **71-100**: The contract exceeds expectations, demonstrating high-quality drafting and comprehensive coverage.\n\n"
    
    "5. **Strengths:**\n"
    "   - Identify specific areas where the contract excels, such as clear language, strong legal safeguards, or innovative provisions.\n\n"
    
    "6. **Weaknesses:**\n"
    "   - Highlight deficiencies or problematic sections that require improvement, such as unclear terms, missing details, or unenforceable clauses.\n\n"
    
    "7. **Ambiguities and Contradictions:**\n"
    "   - Point out any sections or clauses with ambiguous or contradictory language and explain the potential risks or interpretations.\n\n"
    
    "8. **Missing Information:**\n"
    "   - Identify key information or clauses that are absent but necessary for a comprehensive and enforceable agreement.\n\n"
    
    "9. **Constructive Recommendations:**\n"
    "   - Provide practical and actionable suggestions to address weaknesses, resolve ambiguities, and improve the contract's quality.\n\n"
    
    "10. **Professional Tone:**\n"
    "    - Maintain an objective, professional, and constructive tone throughout the report. Avoid judgmental language and focus on providing helpful insights and actionable feedback.\n\n"
    
    "# **Input Details:**\n"
    f"- **Uploaded Contract Text:** {user_text}\n"
    f"- **Relevant Matches from Database:** {top_matches}\n\n"
    
    "# **Output should be in JSON object structure only:**\n"
    "The final report should be structured as a JSON object with the following keys:\n"
    "{\n"
    "    \"Overall Score\": <numerical score>,\n"
    "    \"Reasoning Behind the Score\": <justification for the score>,\n"
    "    \"Legal Compliance\": <analysis of legal compliance>,\n"
    "    \"Strengths\": <list of strengths>,\n"
    "    \"Weaknesses\": <list of weaknesses>,\n"
    "    \"Ambiguities or Contradictions\": <list of ambiguities or contradictions>,\n"
    "    \"Missing Information\": <list of missing or critical clauses>,\n"
    "    \"Areas for Improvement\": <list of actionable suggestions>,\n"
    "    \"Conclusion\": <summary and final recommendation>\n"
    "}\n\n"
    "Ensure that the output contains only the above-mentioned keys and no other words or formatting, that to in json format.\n"
)


    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Analyze the above information and provide a detailed report."}
    ]
    data = {
        "messages": messages,
        "model": "llama3-8b-8192",
        "temperature": 0.7
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ANALYSIS_API_KEY}"
    }
    response = requests.post(ANALYSIS_API_URL, data=json.dumps(data), headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Streamlit UI
st.set_page_config(page_title="Regulatory Compliance Checker", layout="wide")

# Main Sections
st.title("Regulatory Compliance Checker for Legal Contracts")

extracted_text = ""
top_matches = []

# File Upload Section
uploaded_file = st.file_uploader("Upload a contract (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
if uploaded_file is not None:
    try:
        file_type = uploaded_file.name.split(".")[-1].lower()
        if file_type == "pdf":
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif file_type == "docx":
            extracted_text = extract_text_from_docx(uploaded_file)
        elif file_type == "txt":
            extracted_text = uploaded_file.read().decode("utf-8")
            
        else:
            st.error("Unsupported file type.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.warning("Please upload a file to proceed.")
import time
user_text = extracted_text
if extracted_text:
    success_msg = st.success("File uploaded successfully.")
    time.sleep(1)
    success_msg.empty()

st.markdown(
    """
    <hr style="border: 1px solidrgb(253, 108, 76); border-radius: 5px; margin: 20px 0;">
    """,
    unsafe_allow_html=True
)

# Initialize session state variables for navbar control and feature toggles
if "show_key_clauses" not in st.session_state:
    st.session_state.show_key_clauses = False
if "show_analysis" not in st.session_state:
    st.session_state.show_analysis = False
if "active_section" not in st.session_state:
    st.session_state.active_section = "About"  # Default section

import streamlit as st

# Horizontal Navbar with three buttons
left, middle, right = st.columns(3)

if right.button("Extract Key Clauses", use_container_width=True):
    st.session_state.active_section = "Extract Key Clauses"
if middle.button("Analysis Report", use_container_width=True):
    st.session_state.active_section = "Analysis Report"
if left.button("About", use_container_width=True):
    st.session_state.active_section = "About"

# Render content based on active section
if st.session_state.active_section == "About":
    st.header("About the Tool")
    st.markdown("""
        Welcome to the **Regulatory Compliance Checker for Legal Contracts**! This tool is designed to:
        - Extract key clauses from uploaded legal documents.
        - Provide a detailed analysis report based on legal and business standards.
        - Help users identify strengths, weaknesses, and areas for improvement in contracts.

        **Supported Features:**
        - Upload contracts in PDF, DOCX, or TXT formats.
        - Get AI-driven clause extraction and detailed contract analysis.
        - Intuitive interface for legal professionals and businesses.

        Start by uploading a contract to extract key clauses or generate an analysis report.
    """)

elif st.session_state.active_section == "Extract Key Clauses":
    st.header("Extract Key Clauses")
    if extracted_text:
        with st.spinner("Extracting key clauses..."):
            try:
                key_clauses = get_key_clauses(extracted_text)
                st.success("Key clauses extracted successfully!")
                # st.markdown("### Key Clause")
                # st.markdown(f"```json\n{key_clauses}\n```")
                st.markdown("""
<div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px;">
    <pre style="font-size: 14px;">{}</pre>
</div>
""".format(key_clauses), unsafe_allow_html=True)


            except Exception as e:
                st.error(f"Error extracting key clauses: {e}")
    else:
        st.warning("Please upload a file to extract key clauses.")

elif st.session_state.active_section == "Analysis Report":
    if extracted_text:
        if os.path.exists(EMBEDDINGS_PATH):
            with st.spinner("Running Groq Analysis..."):
                embeddings_data = load_embeddings(EMBEDDINGS_PATH)
                top_matches = find_top_matches(extracted_text, embeddings_data)

                for match in top_matches:
                    if "contract" in match["data"]:
                        del match["data"]["contract"]

                analysis_result = analyze_with_groq(user_text, top_matches)
            st.subheader("Detailed Analysis Report")
            st.markdown("""
<div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px;">
    <pre style="font-size: 14px;">{}</pre>
</div>
""".format(analysis_result), unsafe_allow_html=True)
        else:
            st.error("Embeddings file not found.")