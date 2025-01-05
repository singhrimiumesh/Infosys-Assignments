
# YouTube Q&A Chatbot with RAG (Retrieval-Augmented Generation)

## Problem Statement
In this project, we aim to build an intelligent YouTube Q&A chatbot that allows users to interact with YouTube videos by asking questions related to the video content. The chatbot fetches the transcript of a YouTube video and allows users to retrieve relevant information based on their queries. The system leverages Retrieval-Augmented Generation (RAG) techniques to generate context-aware responses, enhancing the user’s experience.

## Approach
We use the following approach to solve the problem:

1. **YouTube Transcript Fetching**: The bot fetches YouTube video transcripts using the `YouTubeTranscriptApi`.
2. **Embedding Generation**: We generate vector embeddings for the transcript chunks using the `SentenceTransformer` model.
3. **FAISS Indexing**: The generated embeddings are indexed using the FAISS library, allowing efficient retrieval of relevant chunks.
4. **Retrieval-Augmented Generation (RAG)**: The chatbot retrieves the most relevant chunks from the transcript based on the user’s query and generates responses using an API (likely OpenAI).
5. **Graphical User Interface (GUI)**: We use PyQt5 to create an interactive desktop application where users can input YouTube video URLs, ask questions, and receive answers.

## Solution
The solution includes:

- A GUI that enables users to input a YouTube URL.
- Fetching and processing of video transcripts.
- Chunking of the transcript and indexing using FAISS for fast retrieval.
- A chatbot interface to interact with the content.
- Using an external API to generate responses based on the transcript chunks retrieved.

## Features
- Fetch and index YouTube video transcripts.
- Ask questions related to the video content.
- Use Retrieval-Augmented Generation (RAG) for accurate and context-aware responses.
- Simple and intuitive graphical user interface (GUI).
- Green button for fetching transcripts and blue button for sending questions.
- Responsive feedback and error handling for invalid URLs.

## Installation

To get started with the YouTube Q&A Chatbot project, follow these installation steps:

### 1. Clone the Repository
```bash
git clone https://github.com/singhrimiumesh/YouTube-Video-Q-A-Chatbot-with-RAG.git
cd YouTube-Video-Q-A-Chatbot-with-RAG
```

### 2. Set up a Virtual Environment
Create and activate a virtual environment to isolate the project dependencies.
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate
```

### 3. Install Required Packages
Install the necessary dependencies using pip:
```bash
pip install -r requirements.txt
```

### 4. Set up Environment Variables
Create a `.env` file in the root directory and add the following entries:
```
API_KEY=your_api_key
url=your_api_url
```

Make sure to replace `your_api_key` and `your_api_url` with actual values.

### 5. Install PyQt5
You can install PyQt5 if it is not already available:
```bash
pip install PyQt5
```

## Usage

### 1. Run the Application
Once all dependencies are installed, run the application by executing the following command:
```bash
python main.py
```

### 2. User Interaction
- **Enter a YouTube video URL** in the input box.
- **Click "Fetch Transcript"** to fetch and index the transcript.
- **Ask questions** related to the content of the video in the input box and click **"Send"** to get a response from the chatbot.

## File Structure

```
YouTube-QA-Chatbot/
├── main.py                  # Main Python script for the application
├── .env                     # Environment file containing API keys and URLs
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Example

### Example Interaction:
- **User**: "What is this video about?"
- **Bot**: "This video is a tutorial about building a Q&A chatbot using YouTube transcripts and Retrieval-Augmented Generation (RAG)."

## Challenges Faced
1. **Handling Long Transcripts**
2. **Embedding Matching Accuracy**
3. **API Integration**

## Acknowledgements
- **YouTube Transcript API**
- **Sentence Transformers**
- **FAISS**
- **PyQt5**
- **OpenAI or LLaMA**
