import os

brain_dir = r'C:\Users\Firza Spector\.gemini\antigravity\brain'

for root, dirs, files in os.walk(brain_dir):
    for file in files:
        if file.endswith('.png') or file.endswith('.webp') or file.endswith('.mp4') or file.endswith('.zip'):
            continue
        path = os.path.join(root, file)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if "FITUR 2" in content or "FITUR 3" in content:
                print(f"Found in: {path}")
        except Exception:
            pass
