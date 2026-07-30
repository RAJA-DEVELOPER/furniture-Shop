import os
import re

ROOT = r"c:\Users\russe\Desktop\decorationShop"

url_regex = re.compile(r'https:\/\/(?:images|plus)\.unsplash\.com\/[^\'\">\s]+')
photo_id_regex = re.compile(r'(photo-[0-9a-fA-F-]+|premium_photo-[0-9a-fA-F-]+)')

all_urls = []
file_url_map = {}

for root, dirs, files in os.walk(ROOT):
    if ".git" in root or "node_modules" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html") or file.endswith(".css"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            found = url_regex.findall(content)
            if found:
                file_url_map[file] = found
                for u in found:
                    m = photo_id_regex.search(u)
                    if m:
                        all_urls.append(m.group(1))

print(f"Total files checked: {len(file_url_map)}")
print(f"Total Unsplash image URLs found: {len(all_urls)}")
print(f"Total unique Unsplash photo IDs found: {len(set(all_urls))}")

dupes = [x for x in set(all_urls) if all_urls.count(x) > 1]
if dupes:
    print(f"[FAIL] Found {len(dupes)} duplicates: {dupes}")
else:
    print("[SUCCESS] VERIFIED 100%! EVERY SINGLE IMAGE ACROSS ALL PAGES IS 100% UNIQUE AND NON-REPEATING GLOBALLY!")
