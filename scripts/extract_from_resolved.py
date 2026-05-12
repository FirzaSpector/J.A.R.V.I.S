import re

path = r'C:\Users\Firza Spector\.gemini\antigravity\brain\351215d7-093d-45e3-a3c6-0ec83062a05c\implementation_plan.md.resolved.3'

try:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"File loaded. Length: {len(text)}")
    
    # Let's search for "function initAudio" and print around it
    for m in re.finditer(r'function\s+initAudio', text):
        start = max(0, m.start() - 100)
        end = min(len(text), m.end() + 3000)
        print("--- Match in resolved.3 ---")
        print(text[start:end])
        print("="*50)
except Exception as e:
    print(f"Error: {e}")
