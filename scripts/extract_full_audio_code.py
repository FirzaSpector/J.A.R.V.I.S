import os

log_path = r"C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c\.system_generated\logs\overview.txt"

if not os.path.exists(log_path):
    print("Log file does not exist!")
    exit(1)

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print(f"Read {len(text)} characters from {log_path}")

# Let's search for "function initAudio" or "async function initAudio"
# Since it might be escaped like \\n, \\", let's search for "initAudio"
pos = 0
while True:
    pos = text.find("initAudio", pos)
    if pos == -1:
        break
    
    print(f"\nFound 'initAudio' at index {pos}")
    # Let's print the surrounding 1000 characters
    start = max(0, pos - 500)
    end = min(len(text), pos + 2500)
    surrounding = text[start:end]
    print("SURROUNDING TEXT:")
    print(surrounding)
    print("=" * 40)
    pos += len("initAudio")
