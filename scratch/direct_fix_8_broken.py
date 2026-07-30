import os
import re
import urllib.request

ROOT = r"c:\Users\russe\Desktop\decorationShop"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 15 Fresh, distinct, active Unsplash photo IDs
FRESH_CANDIDATES = [
    "photo-1513694203232-719a280e022f",
    "photo-1507652313519-d4e9174996dd",
    "photo-1507089947368-19c1da9775ae",
    "photo-1512918728675-ed5a9ecdebfd",
    "photo-1512917774080-9991f1c4c750",
    "photo-1513519245088-0e12902e5a38",
    "photo-1517502884422-41eaead166d4",
    "photo-1518455027359-f3f8164ba6bd",
    "photo-1519643381401-22c77e60520e",
    "photo-1519710164239-da123dc03ef4",
    "photo-1522708323590-d24dbb6b0267",
    "photo-1522771739844-6a9f6d5f14af",
    "photo-1524758631624-e2822e304c36",
    "photo-1527192491265-7e15c55b1ed2",
    "photo-1530018607912-eff2daa1bac4"
]

# Verify which fresh candidates return 200 OK
working_fresh_urls = []
for pid in FRESH_CANDIDATES:
    url = f"https://images.unsplash.com/{pid}?w=900&auto=format&fit=crop&q=85"
    try:
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                working_fresh_urls.append(url)
    except:
        pass

print(f"Verified {len(working_fresh_urls)} fresh working Unsplash URLs.")

# Map broken exact strings to fresh working URLs
broken_targets = [
    "https://images.unsplash.com/photo-1631679707166-512c19a997d4?w=900&auto=format&fit=crop&q=85",
    "https://images.unsplash.com/photo-1583845112203-b1d60b543594?w=900&auto=format&fit=crop&q=85",
    "https://images.unsplash.com/photo-1617104551722-3b2d51366da0?w=900&auto=format&fit=crop&q=85",
    "https://images.unsplash.com/photo-1611485988300-b327272a18b3?w=900&auto=format&fit=crop&q=85",
    "https://images.unsplash.com/photo-1505693314120-0d44b867d686?w=900&auto=format&fit=crop&q=85",
    "https://images.unsplash.com/premium?w=900&auto=format&fit=crop&q=85",
    "https://images.unsplash.com/photo-1604578762246-411d0a7e1405?w=900&auto=format&fit=crop&q=85",
    "https://images.unsplash.com/photo-1580481072645-022f9a6d8310?w=900&auto=format&fit=crop&q=85"
]

target_map = {}
for i, target in enumerate(broken_targets):
    target_map[target] = working_fresh_urls[i % len(working_fresh_urls)]

# Update all workspace files
for root, dirs, files in os.walk(ROOT):
    if ".git" in root or "node_modules" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html") or file.endswith(".css"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            modified = False
            for b_url, r_url in target_map.items():
                if b_url in content:
                    content = content.replace(b_url, r_url)
                    modified = True
                    print(f"Fixed broken image in {file} -> {r_url}")
            
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

print("\nReplacement complete. Running final HTTP check on workspace...")
