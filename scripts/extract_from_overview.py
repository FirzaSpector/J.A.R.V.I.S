import os
import re

log_path = r"C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c\.system_generated\logs\overview.txt"
output_dir = "extracted_steps"
os.makedirs(output_dir, exist_ok=True)

if not os.path.exists(log_path):
    print("Log file does not exist!")
    exit(1)

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's search for the step indices
for step_idx in [918, 934, 980, 1026]:
    print(f"Searching for step_index {step_idx}")
    # Search for "step_index":918 or "step_index": 918
    # Since it's JSON inside logs, it might be escaped, e.g. \"step_index\":918 or similar
    pattern = r'step_index["\\\s:]+' + str(step_idx)
    matches = [m.start() for m in re.finditer(pattern, text)]
    print(f"Found {len(matches)} matches for step {step_idx}")
    for idx, start_pos in enumerate(matches):
        # Extract 100000 characters (plenty of room for entire JSON tool calls)
        snippet = text[start_pos:start_pos + 15000]
        # Let's find the closing brace of the tool call or log entry if possible, or just write it out
        out_name = f"{output_dir}/raw_step_{step_idx}_{idx}.txt"
        with open(out_name, 'w', encoding='utf-8') as out_f:
            out_f.write(snippet)
        print(f"  Wrote {out_name}")
