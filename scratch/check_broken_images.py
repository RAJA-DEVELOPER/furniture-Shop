import os
import re
import urllib.request
import urllib.error

ROOT = r"c:\Users\russe\Desktop\decorationShop"

url_regex = re.compile(r'https:\/\/(?:images|plus)\.unsplash\.com\/[^\'\">\s]+')

all_urls = set()
url_file_map = {}

for root, dirs, files in os.walk(ROOT):
    if ".git" in root or "node_modules" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html") or file.endswith(".css"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            found = url_regex.findall(content)
            for u in found:
                all_urls.add(u)
                if u not in url_file_map:
                    url_file_map[u] = []
                url_file_map[u].append(file)

print(f"Total unique URLs to test: {len(all_urls)}")

broken = []
working = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for i, url in enumerate(sorted(all_urls), 1):
    try:
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                working.append(url)
            else:
                broken.append((url, resp.status))
                print(f"[{i}/{len(all_urls)}] BROKEN ({resp.status}): {url} (in {url_file_map[url]})")
    except urllib.error.HTTPError as e:
        broken.append((url, e.code))
        print(f"[{i}/{len(all_urls)}] BROKEN ({e.code}): {url} (in {url_file_map[url]})")
    except Exception as e:
        broken.append((url, str(e)))
        print(f"[{i}/{len(all_urls)}] ERROR ({e}): {url} (in {url_file_map[url]})")

print(f"\nRESULTS: {len(working)} working, {len(broken)} broken.")
