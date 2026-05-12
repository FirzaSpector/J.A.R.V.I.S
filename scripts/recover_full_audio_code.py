import os
import re

brain_dir = r"C:\Users\Firza Spector\.gemini\antigravity\brain"
output_file = r"c:\jarvis-backend\recovered_audio_functions.txt"

print("Searching recursively for full function bodies of initAudio...")

found_blocks = []

for root, dirs, files in os.walk(brain_dir):
    for file in files:
        if file.endswith("overview.txt") or file.endswith(".md") or file.endswith(".json") or file.endswith(".resolved"):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Look for 'function initAudio'
                idx = 0
                while True:
                    idx = content.find("function initAudio", idx)
                    if idx == -1:
                        break
                    
                    # Extract up to 6000 characters
                    snippet = content[idx:idx+6000]
                    # Let's count how many lines it has
                    lines = snippet.split('\n')
                    # Find if it contains other functions like processClap, wakeJarvis, etc.
                    score = 0
                    if "processClap" in snippet: score += 1
                    if "wakeJarvis" in snippet: score += 1
                    if "playBeep" in snippet: score += 1
                    if "recognition" in snippet: score += 1
                    
                    found_blocks.append({
                        "file": filepath,
                        "score": score,
                        "text": snippet
                    })
                    idx += 18 # move past "function initAudio"
            except Exception as e:
                pass

# Sort found blocks by score, descending
found_blocks.sort(key=lambda x: x["score"], reverse=True)

print(f"Found {len(found_blocks)} occurrences.")
if found_blocks:
    best = found_blocks[0]
    print(f"Best match found in {best['file']} with score {best['score']}")
    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(f"=== SOURCE: {best['file']} ===\n")
        out_f.write(best['text'])
    print(f"Wrote best match to {output_file}")
else:
    print("No matches found.")
