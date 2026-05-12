import os

with open('full_request.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's clean characters that might cause encoding errors on standard Windows terminal print
clean_text = text.replace('\u23f9', '[STOP]')
# Write a clean text file
with open('full_request_clean.txt', 'w', encoding='utf-8') as out:
    out.write(clean_text)

print(f"Total length of text: {len(text)}")
print("Does FITUR 2 exist in full_request.txt?", "FITUR 2" in text)
print("Does FITUR 3 exist in full_request.txt?", "FITUR 3" in text)

# Let's search for "## FITUR" occurrences
import re
for m in re.finditer(r'## FITUR \d:.*', text):
    print(f"Found match: {m.group(0)}")

# Find any line with "FITUR"
for i, line in enumerate(text.splitlines(), 1):
    if "FITUR" in line:
        print(f"Line {i}: {line[:100]}")
