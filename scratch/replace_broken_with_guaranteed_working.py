import os
import re
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = r"c:\Users\russe\Desktop\decorationShop"

url_regex = re.compile(r'https:\/\/(?:images|plus)\.unsplash\.com\/[^\'\">\s]+')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 1. Scan all files for current URLs
all_files = []
file_urls = {}

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
            file_urls[filepath] = found

unique_urls = list(set([u for urls in file_urls.values() for u in urls]))

# 2. Check HTTP status of every URL
def test_url(url):
    try:
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        with urllib.request.urlopen(req, timeout=4) as resp:
            return (url, resp.status == 200)
    except:
        return (url, False)

url_status = {}
with ThreadPoolExecutor(max_workers=30) as executor:
    futures = {executor.submit(test_url, u): u for u in unique_urls}
    for f in as_completed(futures):
        url, ok = f.result()
        url_status[url] = ok

broken_urls = [u for u, ok in url_status.items() if not ok]
print(f"Tested {len(unique_urls)} URLs: {len(unique_urls) - len(broken_urls)} WORKING, {len(broken_urls)} BROKEN.")

if not broken_urls:
    print("[SUCCESS] 100% OF ALL IMAGES ACROSS THE SITE ARE WORKING (HTTP 200 OK)!")
    exit(0)

# Pool of GUARANTEED REAL working Unsplash photo IDs (verified on CDN)
REAL_WORKING_PHOTO_IDS = [
    "photo-1618221195710-dd6b41faaea6",
    "photo-1555041469-a586c61ea9bc",
    "photo-1616594039964-ae9021a400a0",
    "photo-1593642632559-0c6d3fc62b89",
    "photo-1586023492125-27b2c045efd7",
    "photo-1631049307264-da0ec9d70304",
    "photo-1617806118233-18e1de247200",
    "photo-1498409785966-ab341407de6e",
    "photo-1567016432779-094069958ea5",
    "photo-1560448204-603b3fc33ddc",
    "photo-1615066390971-03e4e1c36ddf",
    "photo-1547954575-855750c57bd3",
    "photo-1583847268964-b28dc8f51f92",
    "photo-1600607687939-ce8a6c25118c",
    "photo-1505693416388-ac5ce068fe85",
    "photo-1611269154421-4e27233ac5c7",
    "photo-1600566753190-17f0baa2a6c3",
    "photo-1577140917170-285929fb55b7",
    "photo-1566665797739-1674de7a421a",
    "photo-1497366216548-37526070297c",
    "photo-1512917774080-9991f1c4c750",
    "photo-1600596542815-ffad4c1539a9",
    "photo-1600607687644-c7171b42498f",
    "photo-1600585154526-990dced4db0d",
    "photo-1618219908412-a29a1bb7b86e",
    "photo-1600573472591-ee6b68d14c68",
    "photo-1553484771-898ed465e931",
    "photo-1681949222860-9cb3b0329878",
    "photo-1716703741458-417a8d58f20e",
    "photo-1538688525198-9b88f6f53126",
    "photo-1600585152220-90363fe7e115",
    "photo-1567496898669-ee935f5f647a",
    "photo-1600607687920-4e2a09cf159d",
    "photo-1581291518633-83b4ebd1d83e",
    "photo-1544457070-4cd773b4d71e",
    "photo-1512918728675-ed5a9ecdebfd",
    "photo-1600566752355-35792bedcfea",
    "photo-1513519245088-0e12902e5a38",
    "photo-1541123437800-1bb1317badc2",
    "photo-1513694203232-719a280e022f",
    "photo-1618221381711-42ca8ab6e908",
    "photo-1550581190-9c1c48d21d6c",
    "photo-1600210491892-03d54c0aaf87",
    "photo-1493663284031-b7e3aefcae8e",
    "photo-1549488344-1f9b8d2bd1f3",
    "photo-1533090161767-e6ffed986c88",
    "photo-1594631252845-29fc4cc8cde9",
    "photo-1507652313519-d4e9174996dd",
    "photo-1595526114035-0d45ed16cfbf",
    "photo-1558882224-dda166733046",
    "photo-1522771739844-6a9f6d5f14af",
    "photo-1617325247661-675ab4b64ae2",
    "photo-1530018607912-eff2daa1bac4",
    "photo-1503602642458-232111445657",
    "photo-1519643381401-22c77e60520e",
    "photo-1556911220-e15b29be8c8f",
    "photo-1507089947368-19c1da9775ae",
    "photo-1556909114-f6e7ad7d3136",
    "photo-1524758631624-e2822e304c36",
    "photo-1518455027359-f3f8164ba6bd",
    "photo-1510074377623-8cf13fb86c08",
    "photo-1613545325278-f24b0cae1224",
    "photo-1618220179428-22790b461013",
    "photo-1584100936595-c0654b55a2e2",
    "photo-1507003211169-0a1dd7228f2d",
    "photo-1618219740975-d40978bb7378",
    "photo-1616486029423-aaa4789e8c9a",
    "photo-1585128792020-803d29415281",
    "photo-1565182999561-18d7dc61c393",
    "photo-1527192491265-7e15c55b1ed2",
    "photo-1600566753376-12c8ab7fb75b",
    "photo-1540574163026-643ea20ade25",
    "photo-1532323544230-7191fd51bc1b",
    "photo-1558618666-fcd25c85cd64",
    # Additional tested & working IDs
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
    "photo-1615875605825-5eb9bb5d52ac"
]

# Find IDs currently used by working URLs to prevent duplicate assignments
working_photo_ids = set()
photo_id_regex = re.compile(r'(photo-[0-9a-fA-F-]+|premium_photo-[0-9a-fA-F-]+)')
for u, ok in url_status.items():
    if ok:
        m = photo_id_regex.search(u)
        if m:
            working_photo_ids.add(m.group(1))

# Filter available IDs that are not used by any working image
available_fresh_ids = [pid for pid in REAL_WORKING_PHOTO_IDS if pid not in working_photo_ids]

# Multithreaded check of available fresh IDs to confirm 200 OK
fresh_verified_urls = []

def verify_id(pid):
    if "premium_photo" in pid:
        url = f"https://plus.unsplash.com/{pid}?w=900&auto=format&fit=crop&q=85"
    else:
        url = f"https://images.unsplash.com/{pid}?w=900&auto=format&fit=crop&q=85"
    if test_url(url)[1]:
        return url
    return None

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(verify_id, pid) for pid in available_fresh_ids]
    for f in as_completed(futures):
        res = f.result()
        if res:
            fresh_verified_urls.append(res)

print(f"Found {len(fresh_verified_urls)} fresh, verified working 200 OK URLs.")

# Map broken URLs to fresh verified working URLs
replacement_map = {}
for i, b_url in enumerate(broken_urls):
    if i < len(fresh_verified_urls):
        replacement_map[b_url] = fresh_verified_urls[i]

for filepath in all_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for b_url, r_url in replacement_map.items():
        if b_url in content:
            content = content.replace(b_url, r_url)
            modified = True
            print(f"Replaced broken URL in {os.path.basename(filepath)} with working URL {r_url}")
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("\nAll replacements written. Performing final HTTP status verification on entire workspace...")

# Final verification
final_urls = set()
for filepath in all_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        found = url_regex.findall(f.read())
        final_urls.update(found)

final_broken = []
with ThreadPoolExecutor(max_workers=30) as executor:
    futures = {executor.submit(test_url, u): u for u in final_urls}
    for f in as_completed(futures):
        u, ok = f.result()
        if not ok:
            final_broken.append(u)

if final_broken:
    print(f"[FAIL] Still found {len(final_broken)} broken URLs: {final_broken}")
else:
    print(f"[SUCCESS] 100% VERIFIED! ALL {len(final_urls)} IMAGES ACROSS THE SITE RETURN HTTP 200 OK!")
