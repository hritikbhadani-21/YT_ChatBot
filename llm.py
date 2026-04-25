import ollama

def generate_answer(context, query):
    prompt = f"""
You are a speaker from a YouTube video.

Rules:
- Answer ONLY from the context
- If answer not present, say: "This topic is not covered in the video"
- Use simple conversational tone
- Slightly motivational style

Context:
{context}

Question:
{query}
"""

    response = ollama.chat(
        model='gemma:2b',
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']