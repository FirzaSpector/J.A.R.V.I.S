import os
import re
import json

log_path = r"C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c\.system_generated\logs\overview.txt"
output_dir = "extracted_steps"
os.makedirs(output_dir, exist_ok=True)

if not os.path.exists(log_path):
    print("Log file does not exist!")
    exit(1)

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# We can search for the JSON strings of tool calls
print("Searching for step logs...")
# Let's find step logs by split or regex
steps = re.findall(r'\{"step_index":\d+,"source":"MODEL".*?\}', text, re.DOTALL)
print(f"Found {len(steps)} total steps in log.")

for idx, step_str in enumerate(steps):
    try:
        data = json.loads(step_str)
        step_index = data.get("step_index")
        if step_index in [918, 934, 980, 1026, 234, 237, 244, 247, 483, 484, 485, 486, 487, 488, 489]:
            print(f"Extracting step {step_index}")
            tool_calls = data.get("tool_calls", [])
            for tc_idx, tc in enumerate(tool_calls):
                name = tc.get("name")
                args = tc.get("args", {})
                
                # Write to file
                out_name = f"{output_dir}/step_{step_index}_{name}_{tc_idx}.json"
                with open(out_name, 'w', encoding='utf-8') as out_f:
                    json.dump(tc, out_f, indent=2)
                print(f"  Wrote {out_name}")
    except Exception as e:
        # Some might not be valid JSON if they were truncated in the logs, let's parse using regex
        pass

print("Done extracting steps.")
