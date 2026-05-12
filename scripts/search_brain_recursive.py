import os

brain_dir = r"C:\Users\Firza Spector\.gemini\antigravity\brain"
print("Searching for initAudio recursively...")

found_count = 0
for root, dirs, files in os.walk(brain_dir):
    for file in files:
        if file.endswith("overview.txt") or file.endswith(".html") or file.endswith(".js") or file.endswith(".md") or file.endswith(".json") or file.endswith(".resolved") or file.startswith("implementation_plan") or file.startswith("walkthrough"):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if "initAudio" in content:
                    found_count += 1
                    print(f"\nFOUND '{file}' in {filepath} (size: {len(content)} bytes)")
                    # Find some context
                    idx = content.find("initAudio")
                    start = max(0, idx - 100)
                    end = min(len(content), idx + 2000)
                    print("CONTEXT:")
                    print(content[start:end])
                    print("=" * 60)
                    if found_count >= 10:
                        break
            except Exception as e:
                pass
    if found_count >= 10:
        break
