from dotenv import load_dotenv
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QLabel, QTextBrowser, QMessageBox, QSplitter
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import requests
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from urllib.parse import urlparse
import faiss
from sentence_transformers import SentenceTransformer

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("url")

# Load the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize FAISS index
dimension = 384  
index = faiss.IndexFlatL2(dimension)
transcript_chunks = []  
chunk_metadata = []  

# Function to fetch YouTube transcript
def fetch_transcript(url):
    try:
        video_id = url.split("v=")[1].split("&")[0]
        formatter = JSONFormatter()
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatted_transcript = formatter.format_transcript(transcript)
        
        # Split transcript into smaller chunks
        global transcript_chunks, chunk_metadata
        transcript_chunks = []
        chunk_metadata = []
        chunk_size = 50  # Adjust chunk size based on your needs
        for i in range(0, len(transcript), chunk_size):
            chunk = transcript[i:i+chunk_size]
            chunk_text = " ".join([entry['text'] for entry in chunk])
            transcript_chunks.append(chunk_text)
            chunk_metadata.append({"start": chunk[0]['start'], "end": chunk[-1]['start']})
        
        # Add chunks to FAISS index
        chunk_embeddings = embedding_model.encode(transcript_chunks)
        index.add(chunk_embeddings)
        
        return "Transcript fetched and indexed successfully."
    except Exception as e:
        return f"Error: {e}"

# Retrieve relevant transcript chunks
def retrieve_chunks(query, top_k=3):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    results = [transcript_chunks[i] for i in indices[0] if i < len(transcript_chunks)]
    return results

# API call function
def get_response(prompt, retrieved_chunks):
    system_prompt = (
        f"You are a helpful assistant. Answer questions based on these chunks of transcript:\n"
        f"{' '.join(retrieved_chunks)}"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    data = {
        "messages": messages,
        "model": "llama3-8b-8192",
        "temperature": 0.7
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    try:
        response = requests.post(API_URL, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"API Error: {e}"

# GUI Application
class YouTubeChatBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YouTube Q&A Chatbot with RAG")
        self.setGeometry(100, 100, 900, 600)

        main_layout = QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        # Transcript Fetching
        self.url_label = QLabel("Enter YouTube Video URL:")
        self.url_input = QLineEdit()
        self.fetch_button = QPushButton("Fetch Transcript")
        self.fetch_button.setStyleSheet("background-color: green; color: white;") 
        self.fetch_button.clicked.connect(self.fetch_transcript)
        self.status_label = QLabel("Status: Waiting for input...")

        left_panel.addWidget(self.url_label)
        left_panel.addWidget(self.url_input)
        left_panel.addWidget(self.fetch_button)
        left_panel.addWidget(self.status_label)

        # Chat Interface
        self.chat_area = QTextBrowser()
        self.prompt_label = QLabel("Ask a Question:")
        self.prompt_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background-color: blue; color: white;")  
        self.send_button.clicked.connect(self.send_message)

        right_panel.addWidget(self.chat_area)
        right_panel.addWidget(self.prompt_label)
        right_panel.addWidget(self.prompt_input)
        right_panel.addWidget(self.send_button)

        left_widget = QWidget()
        right_widget = QWidget()
        left_widget.setLayout(left_panel)
        right_widget.setLayout(right_panel)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def fetch_transcript(self):
        url = self.url_input.text().strip()
        if not urlparse(url).scheme in ["http", "https"]:
            QMessageBox.critical(self, "Error", "Invalid URL")
            return

        self.status_label.setText("Status: Fetching transcript...")
        result = fetch_transcript(url)
        self.status_label.setText(result)

    def send_message(self):
        prompt = self.prompt_input.text().strip()
        if not prompt:
            return

        user_message = f'<span style="color: blue;"><br>You:</span> {prompt}' 
        self.chat_area.append(user_message)

        retrieved_chunks = retrieve_chunks(prompt)
        response = get_response(prompt, retrieved_chunks)

        bot_message = f"Bot: {response}"
        self.chat_area.append(bot_message)
        self.prompt_input.clear()

# Main
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    chatbot_app = YouTubeChatBotApp()
    chatbot_app.show()
    sys.exit(app.exec_())
