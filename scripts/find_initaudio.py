import os

target_dir = r'C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c'
found_files = []

for root, dirs, files in os.walk(target_dir):
    for file in files:
        path = os.path.join(root, file)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if "initAudio" in content:
                found_files.append(path)
                print(f"Found initAudio in: {path}")
        except Exception:
            pass

# Also search in other folders
print("Searching other folders...")
brain_dir = r'C:\Users\Firza Spector\.gemini\antigravity\brain'
for root, dirs, files in os.walk(brain_dir):
    for file in files:
        path = os.path.join(root, file)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if "function initAudio" in content:
                print(f"Found 'function initAudio' in: {path}")
        except Exception:
            pass
