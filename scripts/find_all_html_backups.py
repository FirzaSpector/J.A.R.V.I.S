import os

brain_dir = r"C:\Users\Firza Spector\.gemini\antigravity\brain"
print("Scanning brain directory for any HTML files containing 'initAudio'...")

for root, dirs, files in os.walk(brain_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if "initAudio" in content:
                    print(f"FOUND HTML: {path} (size: {len(content)})")
            except Exception:
                pass
