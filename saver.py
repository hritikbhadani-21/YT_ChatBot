def save_text(video_id, text):
    filename = f"{video_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved: {filename}")