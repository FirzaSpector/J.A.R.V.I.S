import os
brain_dir = r"C:\Users\Firza Spector\.gemini\antigravity\brain"
print("Listing all conversation directories under brain:")
for name in os.listdir(brain_dir):
    path = os.path.join(brain_dir, name)
    if os.path.isdir(path):
        print(f" - {name}")
