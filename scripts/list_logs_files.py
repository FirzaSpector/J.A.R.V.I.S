import os

brain_dir = r'C:\Users\Firza Spector\.gemini\antigravity\brain'

for folder in os.listdir(brain_dir):
    folder_path = os.path.join(brain_dir, folder)
    if os.path.isdir(folder_path):
        # List contents of logs
        logs_dir = os.path.join(folder_path, '.system_generated', 'logs')
        if os.path.isdir(logs_dir):
            files = os.listdir(logs_dir)
            print(f"Folder {folder} has logs: {files}")
        else:
            # Check files in folder root
            files = os.listdir(folder_path)
            print(f"Folder {folder} root files: {files}")
