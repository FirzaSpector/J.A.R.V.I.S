import os

brain_dir = r"C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c"
print("Scanning files in target brain folder...")

for root, dirs, files in os.walk(brain_dir):
    for file in files:
        filepath = os.path.join(root, file)
        try:
            size = os.path.getsize(filepath)
            # print if not a system/binary/image file and has size > 0
            if not file.endswith(".png") and not file.endswith(".webp") and size > 0:
                print(f"File: {filepath} ({size} bytes)")
        except Exception as e:
            pass
