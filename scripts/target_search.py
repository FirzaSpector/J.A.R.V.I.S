import os
import json
import re

log_path = r"C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c\.system_generated\logs\overview.txt"
print("Parsing:", log_path)

if not os.path.exists(log_path):
    print("Log file does not exist!")
    exit(1)

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's search for "replace_file_content" after "915" and see what lines are there
# We can search for '"step_index":915' or '"step_index":9' and list step indices around 900-1100
step_matches = re.finditer(r'"step_index":(\d+)', text)
steps_to_extract = []
for m in step_matches:
    val = int(m.group(1))
    if val >= 912:
        steps_to_extract.append((val, m.start()))

print(f"Found {len(steps_to_extract)} steps after 912.")

# For each step, let's extract up to the next step, or 10000 chars, and check if it has replace_file_content
for i in range(len(steps_to_extract)):
    val, start_pos = steps_to_extract[i]
    end_pos = steps_to_extract[i+1][1] if i+1 < len(steps_to_extract) else len(text)
    step_chunk = text[start_pos:end_pos]
    if "replace_file_content" in step_chunk:
        print(f"\n=== STEP {val} HAS REPLACE_FILE_CONTENT ===")
        # Find replace_file_content and print the args
        args_match = re.search(r'"name":"replace_file_content","args":(\{.*?\})', step_chunk, re.DOTALL)
        if args_match:
            try:
                # Let's clean and print the replacement content
                print(step_chunk[:2000]) # Print first 2000 characters of the step log
                print("...")
            except Exception as e:
                print("Error printing chunk:", e)
        else:
            print(step_chunk[:2000])
            print("...")
        print("="*60)
