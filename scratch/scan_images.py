import os
import re

ROOT = r"c:\Users\russe\Desktop\decorationShop"

files_to_check = []
for root, dirs, files in os.walk(ROOT):
    if ".git" in root or "node_modules" in root or "scratch" in root:
        continue
    for f in files:
        if f.endswith(".html") or f.endswith(".css"):
            files_to_check.append(os.path.join(root, f))

print(f"Found {len(files_to_check)} HTML/CSS files.")

url_pattern = re.compile(r'https:\/\/(?:images|plus)\.unsplash\.com\/[^\'\">\s]+')

matches = []
for filepath in files_to_check:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    found = url_pattern.findall(content)
    if found:
        print(f"{os.path.basename(filepath)}: {len(found)} images")
        for m in found:
            matches.append((filepath, m))

print(f"Total image references found across all files: {len(matches)}")
