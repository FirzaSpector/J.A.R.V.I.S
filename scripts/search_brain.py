import os
import json
import re

brain_dir = r'C:\Users\Firza Spector\.gemini\antigravity\brain'
results = []

for folder in os.listdir(brain_dir):
    folder_path = os.path.join(brain_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    
    # We want to check for logs/overview.txt or any text files
    logs_dir = os.path.join(folder_path, '.system_generated', 'logs')
    if os.path.isdir(logs_dir):
        overview_path = os.path.join(logs_dir, 'overview.txt')
        if os.path.isfile(overview_path):
            try:
                with open(overview_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Search for FITUR 1, FITUR 2, FITUR 3 in content
                for word in ["FITUR 1", "FITUR 2", "FITUR 3", "CLAP DETECTION", "WAKE WORD"]:
                    if word in content:
                        # Let's extract some context around it
                        for match in re.finditer(re.escape(word), content):
                            start = max(0, match.start() - 200)
                            end = min(len(content), match.end() + 1000)
                            snippet = content[start:end]
                            results.append({
                                'folder': folder,
                                'word': word,
                                'snippet': snippet
                            })
            except Exception as e:
                print(f"Error reading {overview_path}: {e}")

print(f"Found {len(results)} matches.")
# Save results to a file
with open('brain_search_results.txt', 'w', encoding='utf-8') as out:
    for r in results:
        out.write(f"=== FOLDER: {r['folder']} | WORD: {r['word']} ===\n")
        out.write(r['snippet'])
        out.write("\n\n==================================================\n\n")

print("Done writing to brain_search_results.txt")
