import json

path = r'C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c\.system_generated\logs\overview.txt'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for line in lines:
    if '"step_index":878' in line or '"step_index": 878' in line:
        data = json.loads(line)
        print("data keys:", data.keys())
        tool_calls = data.get("tool_calls", [])
        print("tool_calls len:", len(tool_calls))
        for tc in tool_calls:
            print("tc name:", tc.get("name"))
            args = tc.get("args", {})
            print("args keys:", args.keys())
            for k, v in args.items():
                print(f"arg '{k}' type: {type(v)}")
                if isinstance(v, str) and len(v) < 100:
                    print(f"  val: {v}")
                elif isinstance(v, str):
                    print(f"  val (len={len(v)}): {v[:100]}...")
            
            # If ReplacementChunks is a string, let's load it
            if "ReplacementChunks" in args:
                chunks_val = args["ReplacementChunks"]
                if isinstance(chunks_val, str):
                    try:
                        chunks = json.loads(chunks_val)
                        print("Successfully parsed ReplacementChunks from string! Len:", len(chunks))
                        for i, ch in enumerate(chunks):
                            print(f"Chunk {i+1} keys:", ch.keys())
                    except Exception as ex:
                        print("Error parsing ReplacementChunks string:", ex)
                elif isinstance(chunks_val, list):
                    print("ReplacementChunks is a list. Len:", len(chunks_val))
