import streamlit as st
from extractor import *
from cleaner import clean_text
from rag import chunk_text, create_vector_store, search
from llm import generate_answer

st.set_page_config(page_title="YT RAG Chatbot", layout="wide")

st.title("🎥 YouTube Video Chatbot (RAG + Ollama)")

# ---------------------------
# SESSION STATE
# ---------------------------
if "ready" not in st.session_state:
    st.session_state.ready = False

if "index" not in st.session_state:
    st.session_state.index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "embeddings" not in st.session_state:
    st.session_state.embeddings = None


# ---------------------------
# INPUT SECTION
# ---------------------------
url = st.text_input("Enter YouTube URL")

if st.button("Process Video"):
    if not url:
        st.warning("Please enter a URL")
    else:
        with st.spinner("Processing video..."):

            video_id = extract_video_id(url)

            text = get_transcript(video_id)

            if not text:
                vtt = get_captions(url)
                if vtt:
                    text = clean_vtt(vtt)

            if not text:
                audio = download_audio(url)
                if audio:
                    text = speech_to_text(audio)
                else:
                    st.error("Failed to process video")
                    st.stop()

            # CLEAN
            text = clean_text(text)

            # BUILD RAG
            chunks = chunk_text(text)
            index, embeddings = create_vector_store(chunks)

            # STORE
            st.session_state.index = index
            st.session_state.chunks = chunks
            st.session_state.embeddings = embeddings
            st.session_state.ready = True

        st.success("✅ Video processed! You can now ask questions.")


# ---------------------------
# CHAT SECTION
# ---------------------------
if st.session_state.ready:

    st.subheader("💬 Ask Questions")

    query = st.text_input("Your Question")

    if st.button("Ask"):
        if not query:
            st.warning("Enter a question")
        else:
            with st.spinner("Thinking..."):

                results, distances = search(
                    query,
                    st.session_state.index,
                    st.session_state.chunks,
                    st.session_state.embeddings
                )

                # REJECTION
                if distances[0] > 1.5:
                    st.error("❌ This topic is not covered in the video.")
                else:
                    context = " ".join(results)

                    answer = generate_answer(context, query)

                    st.markdown("### 🧠 Answer")
                    st.write(answer)