with open('brain_search_results.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's check what words were actually found
for line in text.splitlines():
    if "FOLDER:" in line:
        print(line)
    if "FITUR" in line or "Fitur" in line:
        print(f"  {line[:120]}")
