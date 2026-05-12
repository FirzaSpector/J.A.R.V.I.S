import os
import re

path = r'C:\Users\Firza Spector\.gemini\antigravity\brain\8378ffa1-8e5f-4bce-8440-d0370680eea8\.system_generated\logs\overview.txt'
if os.path.exists(path):
    print("Found overview.txt in current conversation. Size:", os.path.getsize(path))
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find positions of "initAudio"
    matches = [m.start() for m in re.finditer('initAudio', content)]
    print(f"Found {len(matches)} occurrences of initAudio in current session")
    for i, pos in enumerate(matches):
        print(f"\n--- Match {i+1} at pos {pos} ---")
        print(content[max(0, pos-400):min(len(content), pos+1600)])
        print("="*60)
else:
    print("Current overview.txt not found")
