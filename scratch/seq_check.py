import os
import re
import urllib.request

ROOT = r"c:\Users\russe\Desktop\decorationShop"

url_regex = re.compile(r'https:\/\/(?:images|plus)\.unsplash\.com\/[^\'\">\s]+')

all_urls = set()
for root, dirs, files in os.walk(ROOT):
    if ".git" in root or "node_modules" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html") or file.endswith(".css"):
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                for u in url_regex.findall(f.read()):
                    all_urls.add(u)

print(f"Checking {len(all_urls)} URLs sequentially with 1.5s timeout...")

headers = {'User-Agent': 'Mozilla/5.0'}

bad_urls = []
for u in sorted(all_urls):
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status not in (200, 301, 302):
                bad_urls.append((u, resp.status))
    except Exception as e:
        bad_urls.append((u, str(e)))

print(f"\nFinal count: {len(all_urls) - len(bad_urls)} SUCCESS, {len(bad_urls)} ERRORS")
if bad_urls:
    print("Failing URLs:")
    for u, err in bad_urls:
        print(f"  {u} -> {err}")
