import os
import json
import re

log_path = r"C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c\.system_generated\logs\overview.txt"

if not os.path.exists(log_path):
    print("Log file does not exist!")
    exit(1)

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find step indices: 878, 918, 934, 980, 1026
target_steps = [878, 918, 934, 980, 1026]

for step in target_steps:
    print(f"\n================ STEP {step} ================")
    # Find '"step_index":<step>'
    pattern = f'"step_index":{step}'
    pos = text.find(pattern)
    if pos == -1:
        print(f"Step {step} not found.")
        continue
    
    # Let's grab the containing line/block.
    # We can find the surrounding brackets { ... } for the JSON object.
    # Let's go backwards to the start of the JSON object
    start_pos = pos
    while start_pos > 0 and text[start_pos] != '{':
        start_pos -= 1
        
    # Now find the matching closing brace, tracking nested braces
    brace_count = 0
    end_pos = start_pos
    while end_pos < len(text):
        if text[end_pos] == '{':
            brace_count += 1
        elif text[end_pos] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_pos += 1
                break
        end_pos += 1
        
    step_json_str = text[start_pos:end_pos]
    try:
        step_json = json.loads(step_json_str)
        # We can extract the tool calls and print their arguments
        for tc in step_json.get("tool_calls", []):
            name = tc.get("name")
            args = tc.get("args", {})
            print(f"Tool call: {name}")
            print(f"Args Keys: {list(args.keys())}")
            # If replacement content or chunks exist, write them to files
            if "ReplacementContent" in args:
                print("Found ReplacementContent!")
                out_fn = f"step_{step}_content.txt"
                with open(out_fn, "w", encoding="utf-8") as out_f:
                    out_f.write(args["ReplacementContent"])
                print(f"  Wrote content to {out_fn}")
            if "ReplacementChunks" in args:
                print("Found ReplacementChunks!")
                out_fn = f"step_{step}_chunks.txt"
                # Since ReplacementChunks might be a stringified JSON array or actual array
                chunks = args["ReplacementChunks"]
                if isinstance(chunks, str):
                    try:
                        chunks = json.loads(chunks)
                    except:
                        pass
                with open(out_fn, "w", encoding="utf-8") as out_f:
                    json.dump(chunks, out_f, indent=2)
                print(f"  Wrote chunks to {out_fn}")
    except Exception as e:
        print(f"Error parsing JSON for step {step}: {e}")
        # Let's write the raw string to a file to examine
        with open(f"step_{step}_raw.txt", "w", encoding="utf-8") as out_f:
            out_f.write(step_json_str)
        print(f"  Wrote raw step string to step_{step}_raw.txt")
