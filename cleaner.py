import re

def remove_repetitions(text):
    return re.sub(r'\b(\w+)( \1\b)+', r'\1', text)

def remove_noise(text):
    return re.sub(r'(.)\1{3,}', r'\1', text)

def normalize(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_text(text):
    text = remove_repetitions(text)
    text = remove_noise(text)
    text = normalize(text)
    return text