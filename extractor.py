import re
import os
import time
import torch
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from transformers import pipeline


def extract_video_id(url):
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"youtube\.com\/shorts\/([0-9A-Za-z_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Invalid URL")


def get_transcript(video_id):
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            t = transcripts.find_manually_created_transcript(['en'])
        except:
            try:
                t = transcripts.find_generated_transcript(['en'])
            except:
                t = next(iter(transcripts))

        data = t.fetch()
        return " ".join([x['text'] for x in data])

    except:
        return None


def get_captions(url):
    try:
        time.sleep(2)

        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'skip_download': True,
            'outtmpl': 'captions',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except:
        return None

    for file in os.listdir():
        if file.endswith(".vtt"):
            return file

    return None


def clean_vtt(file_path):
    text = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and "-->" not in line and "WEBVTT" not in line:
                text.append(line)

    return " ".join(text)


def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir():
        if file.startswith("audio"):
            return file

    return None


def speech_to_text(audio_file):
    device = 0 if torch.cuda.is_available() else -1

    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-base",
        device=device
    )

    result = pipe(audio_file, return_timestamps=True)
    return result["text"]