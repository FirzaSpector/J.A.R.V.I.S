
import json
import os

path = r'C:\Users\Firza Spector\.gemini\antigravity\brain\8378ffa1-8e5f-4bce-8440-d0370680eea8\.system_generated\logs\overview.txt'
with open(path, 'r', encoding='utf-8') as f:
    first_line = f.readline()
    data = json.loads(first_line)
    content = data['content']
    with open('full_request.txt', 'w', encoding='utf-8') as out:
        out.write(content)
