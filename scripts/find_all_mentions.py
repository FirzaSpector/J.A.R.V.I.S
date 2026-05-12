import os

brain_dir = r"C:\Users\Firza Spector\.gemini\antigravity\brain"
print("Scanning brain directory for any files containing 'processClap'...")

for root, dirs, files in os.walk(brain_dir):
    for file in files:
        path = os.path.join(root, file)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if "processClap" in content:
                print(f"FOUND: {path} (size: {len(content)})")
                # print first few occurrences
                idx = content.find("processClap")
                print(f"  Snippet at {idx}: {repr(content[idx-50:idx+200])}")
        except Exception:
            pass
