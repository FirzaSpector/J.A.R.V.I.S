import os

files_to_check = [
    "step_878_raw.txt",
    "step_918_raw.txt",
    "step_934_raw.txt",
    "step_980_raw.txt",
    "step_1026_raw.txt",
    "extracted_steps/raw_step_918_0.txt",
    "extracted_steps/raw_step_934_0.txt",
    "extracted_steps/raw_step_980_0.txt",
    "extracted_steps/raw_step_1026_0.txt"
]

for f_name in files_to_check:
    path = os.path.join(r"c:\jarvis-backend", f_name)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        print(f"File: {f_name} (length: {len(content)})")
        if "initAudio" in content:
            print(f"  FOUND 'initAudio' in {f_name}!")
            # Find all positions
            idx = 0
            while True:
                idx = content.find("initAudio", idx)
                if idx == -1:
                    break
                print(f"    at index {idx}")
                # print 200 chars around it
                start = max(0, idx - 100)
                end = min(len(content), idx + 200)
                print("    SNIPPET:", repr(content[start:end]))
                idx += len("initAudio")
        else:
            print(f"  No 'initAudio' in {f_name}")
