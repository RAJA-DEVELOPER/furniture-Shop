import os
import re
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

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

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def test_url(url):
    try:
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as resp:
            return (url, resp.status, None)
    except urllib.error.HTTPError as e:
        return (url, e.code, None)
    except Exception as e:
        return (url, None, str(e))

broken = []
working = []

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(test_url, u): u for u in all_urls}
    for future in as_completed(futures):
        url, status, err = future.result()
        if status == 200:
            working.append(url)
        else:
            broken.append((url, status, err, url_file_map[url]))

print(f"Tested {len(all_urls)} URLs: {len(working)} WORKING, {len(broken)} BROKEN.\n")
if broken:
    print("BROKEN URLs:")
    for u, status, err, files in broken:
        print(f"  URL: {u}\n  STATUS: {status} ERR: {err}\n  FILES: {files}\n")
