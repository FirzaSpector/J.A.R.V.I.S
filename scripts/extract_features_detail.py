import os
import re
import json

log_path = r"C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c\.system_generated\logs\overview.txt"

if not os.path.exists(log_path):
    print("Log file does not exist!")
    exit(1)

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find step 918, 934, 980, 1026
for step_idx in [918, 934, 980, 1026]:
    print(f"\n==================== STEP {step_idx} ====================")
    pattern = r'"step_index":' + str(step_idx) + r',.*?"tool_calls":(\[.*?\])\}'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        try:
            tool_calls_str = m.group(1)
            # Try to load as JSON to format nicely
            tool_calls = json.loads(tool_calls_str)
            for tool_call in tool_calls:
                print(f"Tool Name: {tool_call.get('name')}")
                args = tool_call.get('args', {})
                print("Args keys:", list(args.keys()))
                for key, val in args.items():
                    if key in ['ReplacementContent', 'ReplacementChunks', 'ReplacementContent', 'TargetContent']:
                        print(f"\n[{key}]:")
                        print(val)
                    else:
                        print(f"[{key}]: {val}")
        except Exception as e:
            print("Regex matched but JSON parsing failed:", e)
            # Fallback to printing the raw match
            print(m.group(0)[:4000])
    else:
        # Try a relaxed search
        pattern_relaxed = r'"step_index":' + str(step_idx) + r',.*?\n'
        m_relaxed = re.search(pattern_relaxed, text)
        if m_relaxed:
            print("Relaxed match:")
            idx = text.find(f'"step_index":{step_idx}')
            if idx == -1:
                idx = text.find(f'"step_index": {step_idx}')
            if idx != -1:
                print(text[idx:idx+4000])
        else:
            print("No match found for step", step_idx)
