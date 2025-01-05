
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

## Technologies Used

- **Python**: The main programming language for the project.
- **PyQt5**: Used for building the graphical user interface (GUI).
- **FAISS**: For efficient similarity search on the transcript embeddings.
- **Sentence-Transformers**: For generating text embeddings to represent the transcript chunks.
- **youtube-transcript-api**: For fetching YouTube video transcripts.
- **requests**: For making HTTP requests to the external chatbot API.
- **python-dotenv**: For managing environment variables.
  
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

### 2. User Interaction
- **Enter a YouTube video URL** in the input box.
- **Click "Fetch Transcript"** to fetch and index the transcript.
- **Ask questions** related to the content of the video in the input box and click **"Send"** to get a response from the chatbot.

## Example

### Example Interaction:
- **User**: "What is this video about?"
- **Bot**: "This video is a tutorial about building a Q&A chatbot using YouTube transcripts and Retrieval-Augmented Generation (RAG)."


## Acknowledgements
- **YouTube Transcript API**
- **Sentence Transformers**
- **FAISS**
- **PyQt5**
- **OpenAI or LLaMA**
