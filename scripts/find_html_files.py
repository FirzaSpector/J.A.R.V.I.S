import os

brain_dir = r"C:\Users\Firza Spector\.gemini\antigravity\brain"
print("Searching for HTML files in brain directory...")

for root, dirs, files in os.walk(brain_dir):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            print(f"FOUND: {filepath} ({os.path.getsize(filepath)} bytes)")
