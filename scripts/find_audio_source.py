import os
import re

brain_dir = r"C:\Users\Firza Spector\.gemini\antigravity\brain"
output_file = r"c:\jarvis-backend\untruncated_audio_code.txt"

print(f"Scanning {brain_dir} for untruncated audio code...")

all_matches = []

for root, dirs, files in os.walk(brain_dir):
    if "8378ffa1-8e5f-4bce-8440-d0370680eea8" in root:
        continue
    for file in files:
        filepath = os.path.join(root, file)
        # Skip some binary files if any
        if file.endswith(('.png', '.webp', '.jpg', '.mp4', '.zip', '.gz')):
            continue
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # We are looking for any occurrence of 'initAudio'
            if "initAudio" in content:
                # Find occurrences where 'function initAudio' is defined
                matches = list(re.finditer(r'(async\s+)?function\s+initAudio', content))
                for m in matches:
                    start_idx = m.start()
                    # Let's extract up to 12000 characters from the match
                    snippet = content[start_idx:start_idx+15000]
                    
                    # Check for truncation markers in this snippet
                    has_trunc = "<truncated" in snippet or "... (initAudio" in snippet or "remain same)" in snippet
                    
                    # Count how many of the target functions are fully defined here
                    targets = ["initAudio", "monitorAudio", "processClap", "wakeJarvis", "playBeep", "recognition", "speak", "loadVoices"]
                    score = sum(1 for t in targets if f"function {t}" in snippet or f"const {t}" in snippet or f"let {t}" in snippet or f"async function {t}" in snippet)
                    
                    # Also count occurrences of these function names in general
                    general_score = sum(1 for t in targets if t in snippet)
                    
                    all_matches.append({
                        "filepath": filepath,
                        "has_trunc": has_trunc,
                        "score": score,
                        "general_score": general_score,
                        "length": len(snippet),
                        "text": snippet
                    })
        except Exception as e:
            pass

# Filter matches: prefer those without truncation, sort by score and general_score
all_matches.sort(key=lambda x: (not x["has_trunc"], x["score"], x["general_score"], x["length"]), reverse=True)

print(f"Found {len(all_matches)} total matches in files.")
if all_matches:
    best = all_matches[0]
    print(f"Best Match File: {best['filepath']}")
    print(f"Has Truncation Markers: {best['has_trunc']}")
    print(f"Target Functions Score: {best['score']}/8")
    print(f"General Score: {best['general_score']}/8")
    
    # Save the best snippet
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(f"=== PATH: {best['filepath']} ===\n")
        out.write(f"=== HAS_TRUNC: {best['has_trunc']} ===\n")
        out.write(best['text'])
    print(f"Wrote best snippet to {output_file}")
else:
    print("No matches found.")
