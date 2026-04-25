## 🎥 YouTube Video RAG Chatbot (Local AI)

Built an end-to-end AI system that transforms any YouTube video into an interactive chatbot.

### 🚀 Features

* Extracts transcript/captions or generates text using Whisper
* Cleans and structures noisy transcript data
* Implements **RAG (Retrieval-Augmented Generation)** using FAISS + embeddings
* Uses **local LLM via Ollama** (no paid APIs)
* Answers strictly from video context (reduces hallucination)
* Rejects out-of-topic queries intelligently
* Mimics speaker’s conversational style
* Streamlit-based UI for real-time interaction

### 🧠 Tech Stack

* Python, Streamlit
* FAISS (Vector DB)
* Sentence Transformers (Embeddings)
* Ollama (Local LLM)
* yt-dlp, YouTube Transcript API
* HuggingFace Transformers

### ⚡ Key Highlight

Optimized pipeline by caching embeddings and vector index, reducing repeated processing time significantly.

### 🎯 Use Case

Turn any long YouTube video (podcasts, lectures, tutorials) into a **queryable knowledge assistant**.
