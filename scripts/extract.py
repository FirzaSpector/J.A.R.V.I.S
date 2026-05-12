import json
import re

path = r'C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c\.system_generated\logs\overview.txt'

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print("File length:", len(content))

# Let's search for step_index 878
idx = content.find('"step_index":878')
if idx == -1:
    idx = content.find('"step_index": 878')

if idx != -1:
    print("Found step_index 878 at pos:", idx)
    # let's grab the surrounding text
    block = content[idx:idx+150000] # Grab a large block since step JSON might be big
    # find the end of this step. Usually steps are separated by newlines or JSON structure
    # Let's write the block to a file
    with open('step_878_found.txt', 'w', encoding='utf-8') as out:
        out.write(block)
else:
    print("Not found step_index 878 directly, let's search for 'step_index' values")
    matches = re.findall(r'"step_index":\s*(\d+)', content)
    print("Available step indices:", sorted(list(set(int(m) for m in matches))))
