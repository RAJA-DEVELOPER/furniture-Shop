import os
import re

ROOT = r"c:\Users\russe\Desktop\decorationShop"

# Pool of distinct high quality Unsplash photo IDs
RAW_POOL = [
    # Index (15)
    "photo-1618221195710-dd6b41faaea6", "photo-1555041469-a586c61ea9bc", "photo-1616594039964-ae9021a400a0",
    "photo-1604578762246-411d0a7e1405", "photo-1593642632559-0c6d3fc62b89", "photo-1586023492125-27b2c045efd7",
    "photo-1631049307264-da0ec9d70304", "photo-1617806118233-18e1de247200", "photo-1498409785966-ab341407de6e",
    "photo-1616486338812-3dadae4b4ace", "photo-1567016432779-094069958ea5", "photo-1560448204-603b3fc33ddc",
    "photo-1615066390971-03e4e1c36ddf", "photo-1547954575-855750c57bd3", "photo-1583847268964-b28dc8f51f92",

    # Home2 (12)
    "photo-1600607687939-ce8a6c25118c", "photo-1580481072645-022f9a6d8310", "photo-1505693416388-ac5ce068fe85",
    "photo-1611269154421-4e27233ac5c7", "photo-1600566753190-17f0baa2a6c3", "photo-1577140917170-285929fb55b7",
    "photo-1566665797739-1674de7a421a", "photo-1497366216548-37526070297c", "photo-1512917774080-9991f1c4c750",
    "photo-1600596542815-ffad4c1539a9", "photo-1600607687644-c7171b42498f", "photo-1600585154526-990dced4db0d",

    # About (8)
    "photo-1618219908412-a29a1bb7b86e", "photo-1600573472591-ee6b68d14c68", "premium_photo-1661331747255-25854e79d9b6",
    "photo-1553484771-898ed465e931", "photo-1681949222860-9cb3b0329878", "photo-1716703741458-417a8d58f20e",
    "photo-1611485988300-b327272a18b3", "photo-1538688525198-9b88f6f53126",

    # Services (12)
    "photo-1600585152220-90363fe7e115", "photo-1567496898669-ee935f5f647a", "photo-1600607687920-4e2a09cf159d",
    "photo-1581291518633-83b4ebd1d83e", "photo-1544457070-4cd773b4d71e", "photo-1512918728675-ed5a9ecdebfd",
    "photo-1600566752355-35792bedcfea", "photo-1513519245088-0e12902e5a38", "photo-1541123437800-1bb1317badc2",
    "photo-1513694203232-719a280e022f", "photo-1618221381711-42ca8ab6e908", "photo-1550581190-9c1c48d21d6c",

    # Gallery (32)
    "photo-1600210491892-03d54c0aaf87", "photo-1493663284031-b7e3aefcae8e", "photo-1549488344-1f9b8d2bd1f3",
    "photo-1533090161767-e6ffed986c88", "photo-1594631252845-29fc4cc8cde9", "photo-1507652313519-d4e9174996dd",
    "photo-1595526114035-0d45ed16cfbf", "photo-1540518614846-7eded433c457", "photo-1558882224-dda166733046",
    "photo-1522771739844-6a9f6d5f14af", "photo-1617325247661-675ab4b64ae2", "photo-1530018607912-eff2daa1bac4",
    "photo-1503602642458-232111445657", "photo-1519643381401-22c77e60520e", "photo-1556911220-e15b29be8c8f",
    "photo-1507089947368-19c1da9775ae", "photo-1556909114-f6e7ad7d3136", "photo-1524758631624-e2822e304c36",
    "photo-1518455027359-f3f8164ba6bd", "photo-1510074377623-8cf13fb86c08", "photo-1613545325278-f24b0cae1224",
    "photo-1618220179428-22790b461013", "photo-1584100936595-c0654b55a2e2", "photo-1507003211169-0a1dd7228f2d",
    "photo-1583845112203-b1d60b543594", "photo-1522708323590-d24dbb6b0267", "photo-1567538096630-e0c55bd6374c",
    "photo-1560185893-a55cbc8c57e8", "photo-1595515106969-1ce29566ff1c", "photo-1578898887932-dce23a595ad4",
    "photo-1519710164239-da123dc03ef4", "photo-1615874959474-d609969a20ed",

    # Blog (13)
    "photo-1618219740975-d40978bb7378", "photo-1616486029423-aaa4789e8c9a", "photo-1615873968403-89e068629265",
    "photo-1585128792020-803d29415281", "photo-1505693314120-0d44b867d686", "photo-1565182999561-18d7dc61c393",
    "photo-1527192491265-7e15c55b1ed2", "photo-1600566753376-12c8ab7fb75b", "photo-1540574163026-643ea20ade25",
    "photo-1532323544230-7191fd51bc1b", "photo-1616137466211-f939a420be84", "photo-1617103996702-96ff29b1c467",
    "photo-1617104551722-3b2d51366da0",

    # Extra backup IDs for single pages & CSS
    "photo-1558618666-fcd25c85cd64", "photo-1631679706909-1844bbd07221", "photo-1631679707166-512c19a997d4",
    "photo-1615875605825-5eb9bb5d52ac", "photo-1616486338812-3dadae4b4ace", "photo-1617103996702-96ff29b1c467",
    "photo-1617104551722-3b2d51366da0", "photo-1618219908412-a29a1bb7b86e", "photo-1618221195710-dd6b41faaea6",
    "photo-1618220179428-22790b461013", "photo-1618221381711-42ca8ab6e908", "photo-1631679706909-1844bbd07221",
    "photo-1631679707166-512c19a997d4", "photo-1600585154340-be6161a56a0c", "photo-1600607687939-ce8a6c25118c",
    "photo-1600566753190-17f0baa2a6c3", "photo-1600596542815-ffad4c1539a9", "photo-1600607687644-c7171b42498f",
    "photo-1600585154526-990dced4db0d", "photo-1600573472591-ee6b68d14c68", "photo-1600585152220-90363fe7e115",
    "photo-1600607687920-4e2a09cf159d", "photo-1600566752355-35792bedcfea", "photo-1600210491892-03d54c0aaf87",
    "photo-1615874959474-d609969a20ed", "photo-1615873968403-89e068629265", "photo-1616137466211-f939a420be84",
    "photo-1631679706909-1844bbd07221", "photo-1631679707166-512c19a997d4", "photo-1615875605825-5eb9bb5d52ac",
    "photo-1513694203232-719a280e022f", "photo-1524758631624-e2822e304c36", "photo-1556911220-e15b29be8c8f",
    "photo-1586023492125-27b2c045efd7", "photo-1560448204-603b3fc33ddc", "photo-1583847268964-b28dc8f51f92",
    "photo-1616594039964-ae9021a400a0", "photo-1604578762246-411d0a7e1405", "photo-1593642632559-0c6d3fc62b89",
    "photo-1631049307264-da0ec9d70304", "photo-1617806118233-18e1de247200", "photo-1498409785966-ab341407de6e",
    "photo-1567016432779-094069958ea5", "photo-1615066390971-03e4e1c36ddf", "photo-1547954575-855750c57bd3",
    "photo-1580481072645-022f9a6d8310", "photo-1505693416388-ac5ce068fe85", "photo-1611269154421-4e27233ac5c7",
    "photo-1577140917170-285929fb55b7", "photo-1566665797739-1674de7a421a", "photo-1497366216548-37526070297c",
    "photo-1512917774080-9991f1c4c750", "photo-1553484771-898ed465e931", "photo-1681949222860-9cb3b0329878",
    "photo-1716703741458-417a8d58f20e", "photo-1611485988300-b327272a18b3", "photo-1538688525198-9b88f6f53126",
    "photo-1567496898669-ee935f5f647a", "photo-1581291518633-83b4ebd1d83e", "photo-1544457070-4cd773b4d71e",
    "photo-1512918728675-ed5a9ecdebfd", "photo-1513519245088-0e12902e5a38", "photo-1541123437800-1bb1317badc2",
    "photo-1550581190-9c1c48d21d6c", "photo-1493663284031-b7e3aefcae8e", "photo-1549488344-1f9b8d2bd1f3",
    "photo-1533090161767-e6ffed986c88", "photo-1594631252845-29fc4cc8cde9", "photo-1507652313519-d4e9174996dd",
    "photo-1595526114035-0d45ed16cfbf", "photo-1540518614846-7eded433c457", "photo-1558882224-dda166733046",
    "photo-1522771739844-6a9f6d5f14af", "photo-1617325247661-675ab4b64ae2", "photo-1530018607912-eff2daa1bac4",
    "photo-1503602642458-232111445657", "photo-1519643381401-22c77e60520e", "photo-1507089947368-19c1da9775ae",
    "photo-1556909114-f6e7ad7d3136", "photo-1510074377623-8cf13fb86c08", "photo-1584100936595-c0654b55a2e2",
    "photo-1507003211169-0a1dd7228f2d", "photo-1583845112203-b1d60b543594", "photo-1522708323590-d24dbb6b0267",
    "photo-1567538096630-e0c55bd6374c", "photo-1560185893-a55cbc8c57e8", "photo-1595515106969-1ce29566ff1c",
    "photo-1578898887932-dce23a595ad4", "photo-1519710164239-da123dc03ef4", "photo-1505693314120-0d44b867d686",
    "photo-1565182999561-18d7dc61c393", "photo-1527192491265-7e15c55b1ed2", "photo-1600566753376-12c8ab7fb75b",
    "photo-1540574163026-643ea20ade25", "photo-1532323544230-7191fd51bc1b",
]

# Ensure we have a set of unique IDs
UNIQUE_IDS = []
for p in RAW_POOL:
    if p not in UNIQUE_IDS:
        UNIQUE_IDS.append(p)

print(f"Total available distinct IDs in pool: {len(UNIQUE_IDS)}")

# Files that need replacements and how many images each file has
FILES_ORDER = [
    ("index.html", 15),
    ("home2.html", 12),
    ("about.html", 8),
    ("services.html", 12),
    ("gallery.html", 32),
    ("blog.html", 13),
    ("contact.html", 1),
    ("login.html", 1),
    ("signup.html", 1),
    ("terms.html", 1),
    ("privacy.html", 1),
    ("sitemap.html", 1),
    ("open-plan-zoning.html", 1),
    ("home-office-design.html", 1),
    ("sustainable-furniture.html", 1),
    ("velvet-upholstery-care.html", 1),
    ("bedroom-colour-palettes.html", 1),
    ("dining-table-guide.html", 1),
    ("css/pages/home.css", 6),
]

assigned_map = {}
idx = 0

for fname, count in FILES_ORDER:
    assigned_map[fname] = []
    for _ in range(count):
        pid = UNIQUE_IDS[idx]
        idx += 1
        # format URL
        if "premium_photo" in pid:
            url = f"https://plus.unsplash.com/{pid}?w=800&auto=format&fit=crop&q=85"
        else:
            url = f"https://images.unsplash.com/{pid}?w=800&auto=format&fit=crop&q=85"
        assigned_map[fname].append(url)

# Double check global uniqueness across all assigned URLs!
all_assigned_urls = []
for fname, urls in assigned_map.items():
    all_assigned_urls.extend(urls)

print(f"Total assigned image URLs: {len(all_assigned_urls)}")
print(f"Unique assigned URLs count: {len(set(all_assigned_urls))}")

if len(all_assigned_urls) != len(set(all_assigned_urls)):
    print("[ERROR] Duplicates found!")
else:
    print("[SUCCESS] 100% DISJOINT UNIQUE UNSPLASH URLs GUARANTEED ACROSS ALL 20 FILES!")
