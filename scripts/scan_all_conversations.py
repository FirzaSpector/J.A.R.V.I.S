import os
import re

brain_dir = r"C:\Users\Firza Spector\.gemini\antigravity\brain"
print("Scanning ALL conversation folders for untruncated function initAudio code...")

all_results = []

for root, dirs, files in os.walk(brain_dir):
    for file in files:
        if file.endswith(('.png', '.webp', '.jpg', '.mp4', '.zip', '.gz')):
            continue
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if "initAudio" in content:
                # Find positions of initAudio
                matches = list(re.finditer(r'function\s+initAudio', content))
                for m in matches:
                    start = m.start()
                    snippet = content[start:start+12000]
                    
                    has_trunc = "<truncated" in snippet or "... (initAudio" in snippet or "remain same)" in snippet
                    
                    # Score based on presence of function definitions or key elements
                    score = 0
                    if "function monitorAudio" in snippet or "async function monitorAudio" in snippet: score += 1
                    if "function processClap" in snippet: score += 1
                    if "function wakeJarvis" in snippet: score += 1
                    if "function playBeep" in snippet: score += 1
                    if "SpeechRecognition" in snippet: score += 1
                    if "speak(" in snippet: score += 1
                    if "function loadVoices" in snippet: score += 1
                    
                    all_results.append({
                        "file": filepath,
                        "has_trunc": has_trunc,
                        "score": score,
                        "length": len(snippet),
                        "snippet": snippet
                    })
        except Exception:
            pass

# Sort: prefer NOT truncated, then higher score, then length
all_results.sort(key=lambda x: (not x["has_trunc"], x["score"], x["length"]), reverse=True)

print(f"Total occurrences found: {len(all_results)}")
if all_results:
    for i, res in enumerate(all_results[:10]):
        print(f"\n[{i+1}] File: {res['file']}")
        print(f"    Has Truncation Markers: {res['has_trunc']}")
        print(f"    Score: {res['score']}/7")
        print(f"    Snippet length: {res['length']}")
        print("    Preview:")
        print(res['snippet'][:500] + "...")
        print("-" * 60)
        
    # Write the best one to a dedicated file
    best = all_results[0]
    with open("best_found_audio_code.txt", "w", encoding="utf-8") as out:
        out.write(f"=== BEST MATCH SOURCE: {best['file']} ===\n")
        out.write(f"=== HAS_TRUNC: {best['has_trunc']} ===\n")
        out.write(f"=== SCORE: {best['score']} ===\n\n")
        out.write(best['snippet'])
    print("\nSaved best match to best_found_audio_code.txt")
else:
    print("No occurrences found at all.")
