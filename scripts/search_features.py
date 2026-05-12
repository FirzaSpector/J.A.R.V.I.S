
import json
import re

path = r'C:\Users\Firza Spector\.gemini\antigravity\brain\8378ffa1-8e5f-4bce-8440-d0370680eea8\.system_generated\logs\overview.txt'
with open(path, 'r', encoding='utf-8') as f:
    first_line = f.readline()
    data = json.loads(first_line)
    content = data['content']
    
    # Check if content has "truncated" markers
    if "<truncated" in content:
        print("CONTENT IS TRUNCATED IN LOG")
    
    # Try to find FITUR 2 and 3
    match2 = re.search(r"## FITUR 2: (.*)", content)
    match3 = re.search(r"## FITUR 3: (.*)", content)
    
    if match2:
        print(f"FITUR 2: {match2.group(1)}")
    else:
        print("FITUR 2 NOT FOUND")
        
    if match3:
        print(f"FITUR 3: {match3.group(1)}")
    else:
        print("FITUR 3 NOT FOUND")
        
    # Print the last 500 chars before truncation if it exists
    trunc_pos = content.find("<truncated")
    if trunc_pos != -1:
        print("--- BEFORE TRUNCATION ---")
        print(content[max(0, trunc_pos-500):trunc_pos])
