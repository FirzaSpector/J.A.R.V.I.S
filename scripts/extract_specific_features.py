with open('brain_recursive_search.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's split by the delimiter
sections = text.split("==================================================")
print(f"Total sections: {len(sections)}")

for i, s in enumerate(sections):
    if "FITUR 2" in s or "FITUR 3" in s:
        # Check if this contains the actual list or specifications
        if "CLAP" in s or "WAKE" in s or "VOICE" in s or "SPEECH" in s or "SSE" in s:
            print(f"\n--- USEFUL SECTION {i} ---")
            # Get path
            path_line = s.strip().splitlines()[0] if s.strip() else ""
            print(f"Path: {path_line}")
            print(s[:1000]) # Print first 1000 characters of the section
            print("-" * 50)
