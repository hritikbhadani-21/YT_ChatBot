from extractor import *
from cleaner import clean_text
from saver import save_text
from rag import chunk_text, create_vector_store, search
from llm import generate_answer


def main():
    url = input("Enter YouTube URL: ").strip()

    video_id = extract_video_id(url)

    print("STEP 1: Transcript")
    text = get_transcript(video_id)

    if not text:
        print("STEP 2: Captions")
        vtt = get_captions(url)
        if vtt:
            text = clean_vtt(vtt)

    if not text:
        print("STEP 3: Audio → Whisper")
        audio = download_audio(url)
        if audio:
            text = speech_to_text(audio)
        else:
            print("❌ Failed")
            return

    # CLEAN TEXT
    text = clean_text(text)

    # SAVE TEXT (optional)
    save_text(video_id, text)

    print("\n📚 Building RAG system...")
    chunks = chunk_text(text)
    index, embeddings = create_vector_store(chunks)

    print("\n🤖 Chatbot Ready!")

    while True:
        query = input("\nAsk a question (type 'exit'): ")

        if query.lower() == "exit":
            break

        results, distances = search(query, index, chunks, embeddings)

        # 🔴 REJECTION LOGIC
        if distances[0] > 1.5:
            print("❌ This topic is not covered in the video.")
            continue

        context = " ".join(results)

        answer = generate_answer(context, query)

        print("\n🧠 Answer:")
        print(answer)


if __name__ == "__main__":
    main()