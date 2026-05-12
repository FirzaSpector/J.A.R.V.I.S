import json
import re

with open('step_878_found.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Since text might contain multiple JSON records or one big block, let's try to extract the JSON object.
# The overview.txt has entries of the form: {"step_index":878, ...}
# Let's find the first '{' before "step_index":878 and the matching '}' or just parse it as line-by-line JSON.
# Wait, let's look at how overview.txt stores it.
# Let's write a python parser to extract the "multi_replace_file_content" argument or any ReplacementChunks.
# We will look for any JSON block.

try:
    # Let's find the start of the JSON object (which starts with {"step_index":878 or similar)
    # Since we grabbed content starting from "step_index":878, we can prepend '{"' to make it a valid JSON or parse it.
    # Actually, let's find the exact line in overview.txt.
    path = r'C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c\.system_generated\logs\overview.txt'
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    found_line = None
    for line in lines:
        if '"step_index":878' in line or '"step_index": 878' in line:
            found_line = line
            break
            
    if found_line:
        print("Found line for step 878!")
        data = json.loads(found_line)
        tool_calls = data.get("tool_calls", [])
        for tc in tool_calls:
            if tc.get("name") == "multi_replace_file_content":
                args = tc.get("args", {})
                chunks = args.get("ReplacementChunks", [])
                print(f"Found {len(chunks)} replacement chunks!")
                for i, chunk in enumerate(chunks):
                    print(f"\n--- Chunk {i+1} ---")
                    print("Start:", chunk.get("StartLine"), "End:", chunk.get("EndLine"))
                    print("Target:")
                    print(chunk.get("TargetContent"))
                    print("Replacement:")
                    print(chunk.get("ReplacementContent"))
                    print("-" * 50)
                    
                    with open(f'recovered_chunk_{i+1}.txt', 'w', encoding='utf-8') as chunk_out:
                        chunk_out.write(chunk.get("ReplacementContent", ""))
    else:
        print("Could not find line in overview.txt with step 878 directly")
except Exception as e:
    print("Error parsing:", e)
