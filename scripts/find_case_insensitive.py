import os
import re

brain_dir = r'C:\Users\Firza Spector\.gemini\antigravity\brain'

for root, dirs, files in os.walk(brain_dir):
    for file in files:
        if file.endswith('.png') or file.endswith('.webp') or file.endswith('.mp4') or file.endswith('.zip'):
            continue
        path = os.path.join(root, file)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Let's search for "fitur" followed by 2 or 3 case-insensitively
            m2 = re.search(r'fitur\s*2', content, re.IGNORECASE)
            m3 = re.search(r'fitur\s*3', content, re.IGNORECASE)
            
            if m2 or m3:
                print(f"Found in: {path}")
                if m2:
                    start = max(0, m2.start() - 100)
                    end = min(len(content), m2.end() + 1000)
                    print(f"--- FITUR 2 MATCH ---")
                    print(content[start:end])
                if m3:
                    start = max(0, m3.start() - 100)
                    end = min(len(content), m3.end() + 1000)
                    print(f"--- FITUR 3 MATCH ---")
                    print(content[start:end])
                print("=" * 80)
        except Exception:
            pass
