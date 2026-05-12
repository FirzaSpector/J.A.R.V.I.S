import os

input_path = r"c:\jarvis-backend\untruncated_audio_code.txt"
output_path = r"c:\jarvis-backend\formatted_audio_code.txt"

if os.path.exists(input_path):
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Let's replace literal '\n' and '\\n' with actual newlines
    formatted = content.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
    
    # Write it out with normal lines
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(formatted)
    print(f"Successfully formatted to {output_path}")
else:
    print("Input path not found.")
