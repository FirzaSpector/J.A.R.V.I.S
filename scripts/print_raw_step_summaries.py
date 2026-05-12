import os

files_to_check = [
    "step_878_raw.txt",
    "step_918_raw.txt",
    "step_934_raw.txt",
    "step_980_raw.txt",
    "step_1026_raw.txt",
]

for f_name in files_to_check:
    path = os.path.join(r"c:\jarvis-backend", f_name)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        print(f"=== {f_name} ===")
        print(content[:600])
        print("="*40)
