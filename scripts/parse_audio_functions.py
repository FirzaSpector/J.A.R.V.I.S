with open('extracted_audio_functions.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for "function initAudio" and extract up to the end of functions or 2000 characters
import re
for m in re.finditer(r'function\s+initAudio', text):
    start = m.start()
    end = start + 3500
    snippet = text[start:end]
    print("--- SNIPPET FOR INITAUDIO ---")
    print(snippet)
    print("*" * 80)
