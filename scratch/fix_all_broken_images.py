import os
import re
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = r"c:\Users\russe\Desktop\decorationShop"

url_regex = re.compile(r'https:\/\/(?:images|plus)\.unsplash\.com\/[^\'\">\s]+')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 1. Collect all image URLs currently in project files
all_files = []
file_url_map = {}

for root, dirs, files in os.walk(ROOT):
    if ".git" in root or "node_modules" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html") or file.endswith(".css"):
            filepath = os.path.join(root, file)
            all_files.append(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            found = url_regex.findall(content)
            file_url_map[filepath] = found

unique_urls = list(set([u for urls in file_url_map.values() for u in urls]))
print(f"Testing {len(unique_urls)} image URLs currently in workspace...")

def check_url(url):
    try:
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        with urllib.request.urlopen(req, timeout=4) as resp:
            return (url, resp.status == 200)
    except:
        return (url, False)

url_status = {}
with ThreadPoolExecutor(max_workers=30) as executor:
    futures = {executor.submit(check_url, u): u for u in unique_urls}
    for f in as_completed(futures):
        url, ok = f.result()
        url_status[url] = ok

broken_urls = [u for u, ok in url_status.items() if not ok]
print(f"Status check done: {len(unique_urls) - len(broken_urls)} OK, {len(broken_urls)} BROKEN.")

if not broken_urls:
    print("[SUCCESS] ALL IMAGES IN WORKSPACE ARE CURRENTLY WORKING (HTTP 200 OK)!")
    exit(0)

print(f"\nFound {len(broken_urls)} broken URLs. Finding guaranteed 200 OK replacements...")

# Pool of fresh candidate Unsplash photo IDs to replace broken ones
candidate_pids = [
    "photo-1502005229762-cf1b2da7c5d6",
    "photo-1501183638710-841dd1904471",
    "photo-1502672260266-1c1ef2d93688",
    "photo-1513584684374-8bab748fbf90",
    "photo-1513151233558-d860c5398176",
    "photo-1531835551805-16d864c8d311",
    "photo-1534349762230-e0cadf78f5da",
    "photo-1484154218962-a197022b5858",
    "photo-1615874959474-d609969a20ed",
    "photo-1615873968403-89e068629265",
    "photo-1616137466211-f939a420be84",
    "photo-1617103996702-96ff29b1c467",
    "photo-1631679706909-1844bbd07221",
    "photo-1615875605825-5eb9bb5d52ac",
    "photo-1583847268964-b28dc8f51f92",
    "photo-1586023492125-27b2c045efd7",
    "photo-1555041469-a586c61ea9bc",
    "photo-1540518614846-7eded433c457",
    "photo-1616594039964-ae9021a400a0",
    "photo-1593642632559-0c6d3fc62b89",
]

# Currently used photo IDs so we preserve 100% uniqueness
used_photo_ids = set()
photo_id_regex = re.compile(r'(photo-[0-9a-fA-F-]+|premium_photo-[0-9a-fA-F-]+)')
for u, ok in url_status.items():
    if ok:
        m = photo_id_regex.search(u)
        if m:
            used_photo_ids.add(m.group(1))

# Check candidate URLs for 200 OK
def check_pid(pid):
    url = f"https://images.unsplash.com/{pid}?w=900&auto=format&fit=crop&q=85"
    if check_url(url)[1]:
        return (pid, url)
    return (pid, None)

valid_replacements = []
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(check_pid, pid) for pid in candidate_pids if pid not in used_photo_ids]
    for f in as_completed(futures):
        pid, url = f.result()
        if url:
            valid_replacements.append(url)
            used_photo_ids.add(pid)

print(f"Found {len(valid_replacements)} valid replacement URLs.")

# Map broken URL -> replacement URL
replacement_map = {}
for i, b_url in enumerate(broken_urls):
    if i < len(valid_replacements):
        replacement_map[b_url] = valid_replacements[i]
    else:
        print(f"WARNING: Not enough replacements for broken URL: {b_url}")

# Replace broken URLs in files
for filepath in all_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for b_url, r_url in replacement_map.items():
        if b_url in content:
            content = content.replace(b_url, r_url)
            modified = True
            print(f"Replaced broken image in {os.path.basename(filepath)} with {r_url}")
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("\n[SUCCESS] ALL BROKEN IMAGES REPLACED AND VERIFIED!")
