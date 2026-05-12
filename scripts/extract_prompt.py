import json

path = r'C:\Users\Firza Spector\.gemini\antigravity\brain\8378ffa1-8e5f-4bce-8440-d0370680eea8\.system_generated\logs\overview.txt'

with open(path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f, 1):
        if 'Kamu adalah senior frontend developer.' in line:
            print(f"Found on line: {line_idx}")
            # Try parsing the JSON line
            try:
                data = json.loads(line)
                content = data.get('content', '')
                print("--- CONTENT ---")
                # Write to a file so we can view it cleanly without CP1252 encoding issues
                with open('extracted_user_prompt.txt', 'w', encoding='utf-8') as out:
                    out.write(content)
                print(f"Extracted prompt length: {len(content)}. Saved to extracted_user_prompt.txt")
            except Exception as e:
                print(f"Error parsing: {e}")
            break
