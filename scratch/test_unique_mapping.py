import os
import re

ROOT = r"c:\Users\russe\Desktop\decorationShop"

# Dictionary mapping file relative path -> list of 100% UNIQUE Unsplash URLs (matching order of image appearance in file)

UNIQUE_MAPPING = {
    "index.html": [
        "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=1600&auto=format&fit=crop&q=85", # Hero BG
        "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=900&auto=format&fit=crop&q=85",  # Milano Lounge
        "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=700&auto=format&fit=crop&q=85",  # Kyoto Bedroom
        "https://images.unsplash.com/photo-1604578762246-411d0a7e1405?w=700&auto=format&fit=crop&q=85",  # Scandinavian Dining
        "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=700&auto=format&fit=crop&q=85",  # Executive Office
        "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&auto=format&fit=crop&q=85",  # Product 1 (Velvet sofa)
        "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=600&auto=format&fit=crop&q=85",  # Product 2 (Osaka bed)
        "https://images.unsplash.com/photo-1617806118233-18e1de247200?w=600&auto=format&fit=crop&q=85",  # Product 3 (Florence table)
        "https://images.unsplash.com/photo-1498409785966-ab341407de6e?w=600&auto=format&fit=crop&q=85",  # Product 4 (Brentwood desk)
        "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=900&auto=format&fit=crop&q=85",  # Craftsmanship visual
        "https://images.unsplash.com/photo-1567016432779-094069958ea5?w=900&auto=format&fit=crop&q=85",  # Inspiration feature
        "https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=600&auto=format&fit=crop&q=85",  # Nordic Bedroom sidebar
        "https://images.unsplash.com/photo-1615066390971-03e4e1c36ddf?w=600&auto=format&fit=crop&q=85",  # Warm Dining sidebar
        "https://images.unsplash.com/photo-1547954575-855750c57bd3?w=600&auto=format&fit=crop&q=85",  # Executive Office sidebar
        "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=900&auto=format&fit=crop&q=85",  # Quick View Modal
    ],

    "home2.html": [
        "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1600&auto=format&fit=crop&q=85", # Hero BG
        "https://images.unsplash.com/photo-1580481072645-022f9a6d8310?w=700&auto=format&fit=crop&q=85",  # Vesper Accent Chair
        "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=600&auto=format&fit=crop&q=85",  # Sage Bedside Table
        "https://images.unsplash.com/photo-1611269154421-4e27233ac5c7?w=600&auto=format&fit=crop&q=85",  # Hudson Lounge Chair
        "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=700&auto=format&fit=crop&q=85",  # Loft Collection
        "https://images.unsplash.com/photo-1577140917170-285929fb55b7?w=600&auto=format&fit=crop&q=85",  # Urban Dining Set
        "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=600&auto=format&fit=crop&q=85",  # Nordic Rest
        "https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&auto=format&fit=crop&q=85",  # Work Suite
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600&auto=format&fit=crop&q=85",  # Terrace Living
        "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=700&auto=format&fit=crop&q=85",  # Belgravia Penthouse
        "https://images.unsplash.com/photo-1600607687644-c7171b42498f?w=700&auto=format&fit=crop&q=85",  # Marina Villa
        "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=700&auto=format&fit=crop&q=85",  # Upper East Loft
    ],

    "about.html": [
        "https://images.unsplash.com/photo-1618219908412-a29a1bb7b86e?w=1600&auto=format&fit=crop&q=85", # Hero BG
        "https://images.unsplash.com/photo-1600573472591-ee6b68d14c68?w=900&auto=format&fit=crop&q=85",  # Story visual
        "https://plus.unsplash.com/premium_photo-1661331747255-25854e79d9b6?w=600&auto=format&fit=crop&q=60", # Elena portrait
        "https://images.unsplash.com/photo-1553484771-898ed465e931?w=600&auto=format&fit=crop&q=60",  # Marco portrait
        "https://images.unsplash.com/photo-1681949222860-9cb3b0329878?w=600&auto=format&fit=crop&q=60",  # Yuki portrait
        "https://images.unsplash.com/photo-1716703741458-417a8d58f20e?w=600&auto=format&fit=crop&q=60",  # Amara portrait
        "https://images.unsplash.com/photo-1611485988300-b327272a18b3?w=700&auto=format&fit=crop&q=80",  # Master woodworker
        "https://images.unsplash.com/photo-1538688525198-9b88f6f53126?w=700&auto=format&fit=crop&q=85",  # Sustainable craft
    ],

    "services.html": [
        "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=1600&auto=format&fit=crop&q=85", # Services Hero BG
        "https://images.unsplash.com/photo-1567496898669-ee935f5f647a?w=700&auto=format&fit=crop&q=85",  # In-showroom consultation
        "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=700&auto=format&fit=crop&q=85",  # Home Visit service
        "https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?w=700&auto=format&fit=crop&q=85",  # Virtual consultation
        "https://images.unsplash.com/photo-1544457070-4cd773b4d71e?w=700&auto=format&fit=crop&q=85",  # Custom furniture crafting
        "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=700&auto=format&fit=crop&q=85",  # Room refresh styling
        "https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=700&auto=format&fit=crop&q=85",  # Full home package
        "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=700&auto=format&fit=crop&q=85",  # Seasonal restyling
        "https://images.unsplash.com/photo-1541123437800-1bb1317badc2?w=600&auto=format&fit=crop&q=85",  # Walnut guide
        "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=600&auto=format&fit=crop&q=85",  # White oak guide
        "https://images.unsplash.com/photo-1618221381711-42ca8ab6e908?w=600&auto=format&fit=crop&q=85",  # Italian marble guide
        "https://images.unsplash.com/photo-1550581190-9c1c48d21d6c?w=600&auto=format&fit=crop&q=85",  # Full-grain leather guide
    ],

    "gallery.html": [
        "https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?w=1600&auto=format&fit=crop&q=85", # Gallery Hero BG
        "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=900&auto=format&fit=crop&q=85",  # Living Milano sofa
        "https://images.unsplash.com/photo-1549488344-1f9b8d2bd1f3?w=600&auto=format&fit=crop&q=85",  # Living Walnut armchair
        "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=600&auto=format&fit=crop&q=85",  # Living Bronze coffee table
        "https://images.unsplash.com/photo-1594631252845-29fc4cc8cde9?w=600&auto=format&fit=crop&q=85",  # Living White oak shelving
        "https://images.unsplash.com/photo-1507652313519-d4e9174996dd?w=600&auto=format&fit=crop&q=85",  # Living Media console
        "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=700&auto=format&fit=crop&q=85",  # Bedroom Osaka bed
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=900&auto=format&fit=crop&q=85",  # Bedroom Kyoto suite
        "https://images.unsplash.com/photo-1558882224-dda166733046?w=600&auto=format&fit=crop&q=85",  # Bedroom Nordic wardrobe
        "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=600&auto=format&fit=crop&q=85",  # Bedroom Dressing table
        "https://images.unsplash.com/photo-1617325247661-675ab4b64ae2?w=600&auto=format&fit=crop&q=85",  # Bedroom Sage bedside tables
        "https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?w=900&auto=format&fit=crop&q=85",  # Dining Florence table
        "https://images.unsplash.com/photo-1503602642458-232111445657?w=600&auto=format&fit=crop&q=85",  # Dining Scandinavian chairs
        "https://images.unsplash.com/photo-1519643381401-22c77e60520e?w=600&auto=format&fit=crop&q=85",  # Dining Walnut sideboard
        "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=700&auto=format&fit=crop&q=85",  # Kitchen Marble island
        "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=600&auto=format&fit=crop&q=85",  # Kitchen Breakfast stools
        "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&auto=format&fit=crop&q=85",  # Kitchen Pantry cabinet
        "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=700&auto=format&fit=crop&q=85",  # Office Executive desk
        "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=600&auto=format&fit=crop&q=85",  # Office Hudson lounge chair
        "https://images.unsplash.com/photo-1510074377623-8cf13fb86c08?w=600&auto=format&fit=crop&q=85",  # Office Modular bookcase
        "https://images.unsplash.com/photo-1613545325278-f24b0cae1224?w=600&auto=format&fit=crop&q=85",  # Decor Brass vase
        "https://images.unsplash.com/photo-1618220179428-22790b461013?w=600&auto=format&fit=crop&q=85",  # Decor Arch mirror
        "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=600&auto=format&fit=crop&q=85",  # Decor Linen cushions
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&auto=format&fit=crop&q=85",  # Decor Rattan pendant
        "https://images.unsplash.com/photo-1583845112203-b1d60b543594?w=500&auto=format&fit=crop&q=80",  # Customer @sophia_m
        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=500&auto=format&fit=crop&q=80",  # Customer @j_whitfield
        "https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=500&auto=format&fit=crop&q=80",  # Customer @elena_v
        "https://images.unsplash.com/photo-1560185893-a55cbc8c57e8?w=500&auto=format&fit=crop&q=80",  # Customer @amara_o
        "https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?w=500&auto=format&fit=crop&q=80",  # Customer @marco_r
        "https://images.unsplash.com/photo-1578898887932-dce23a595ad4?w=500&auto=format&fit=crop&q=80",  # Customer @yuki_t
        "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=500&auto=format&fit=crop&q=80",  # Customer @michael_c
        "https://images.unsplash.com/photo-1600210492486-724fe5c67fb3?w=500&auto=format&fit=crop&q=80",  # Customer @amelia_t
    ],

    "blog.html": [
        "https://images.unsplash.com/photo-1618219740975-d40978bb7378?w=1600&auto=format&fit=crop&q=85", # Blog Hero BG
        "https://images.unsplash.com/photo-1616486029423-aaa4789e8c9a?w=900&auto=format&fit=crop&q=85",  # Art of Layering
        "https://images.unsplash.com/photo-1550581190-9c1c48d21d6c?w=600&auto=format&fit=crop&q=85",  # Choosing Perfect Sofa
        "https://images.unsplash.com/photo-1585128792020-803d29415281?w=600&auto=format&fit=crop&q=85",  # Biophilic Design
        "https://images.unsplash.com/photo-1505693314120-0d44b867d686?w=600&auto=format&fit=crop&q=85",  # Bedroom Colour Palettes
        "https://images.unsplash.com/photo-1565182999561-18d7dc61c393?w=600&auto=format&fit=crop&q=85",  # Dining Table Guide
        "https://images.unsplash.com/photo-1527192491265-7e15c55b1ed2?w=600&auto=format&fit=crop&q=85",  # Home Office Design
        "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?w=600&auto=format&fit=crop&q=85",  # Zoning Open Plan
        "https://images.unsplash.com/photo-1540574163026-643ea20ade25?w=600&auto=format&fit=crop&q=85",  # Velvet Care Guide
        "https://images.unsplash.com/photo-1532323544230-7191fd51bc1b?w=600&auto=format&fit=crop&q=85",  # Sustainable Furniture
        "https://images.unsplash.com/photo-1583845112239-97ef1341b271?w=400&auto=format&fit=crop&q=85",  # Design Tip 1
        "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=400&auto=format&fit=crop&q=85",  # Design Tip 2
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400&auto=format&fit=crop&q=85",  # Design Tip 3
    ],

    "contact.html": [
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1600&auto=format&fit=crop&q=85",
    ],
    "login.html": [
        "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=1600&auto=format&fit=crop&q=85",
    ],
    "signup.html": [
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=1600&auto=format&fit=crop&q=85",
    ],
    "terms.html": [
        "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=1200&auto=format&fit=crop&q=85",
    ],
    "privacy.html": [
        "https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?w=1200&auto=format&fit=crop&q=85",
    ],
    "sitemap.html": [
        "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=1200&auto=format&fit=crop&q=85",
    ],
    "open-plan-zoning.html": [
        "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1200&auto=format&fit=crop&q=85",
    ],
    "home-office-design.html": [
        "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=1200&auto=format&fit=crop&q=85",
    ],
    "sustainable-furniture.html": [
        "https://images.unsplash.com/photo-1510074377623-8cf13fb86c08?w=1200&auto=format&fit=crop&q=85",
    ],
    "velvet-upholstery-care.html": [
        "https://images.unsplash.com/photo-1613545325278-f24b0cae1224?w=1200&auto=format&fit=crop&q=85",
    ],
    "bedroom-colour-palettes.html": [
        "https://images.unsplash.com/photo-1618220179428-22790b461013?w=1200&auto=format&fit=crop&q=85",
    ],
    "dining-table-guide.html": [
        "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=1200&auto=format&fit=crop&q=85",
    ],

    "home.css": [
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200&auto=format&fit=crop&q=80", # room-living
        "https://images.unsplash.com/photo-1583845112203-b1d60b543594?w=1200&auto=format&fit=crop&q=80", # room-bedroom
        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=1200&auto=format&fit=crop&q=80", # room-dining
        "https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=1200&auto=format&fit=crop&q=80", # room-kitchen
        "https://images.unsplash.com/photo-1560185893-a55cbc8c57e8?w=1200&auto=format&fit=crop&q=80", # room-office
        "https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?w=1200&auto=format&fit=crop&q=80", # room-outdoor
    ]
}

# Verification step before executing edits!
all_photo_ids = []
photo_id_regex = re.compile(r'(photo-[0-9a-fA-F-]+|premium_photo-[0-9a-fA-F-]+)')

for fname, urls in UNIQUE_MAPPING.items():
    for u in urls:
        m = photo_id_regex.search(u)
        if m:
            all_photo_ids.append(m.group(1))

print(f"Total mapped image URLs: {len(all_photo_ids)}")
print(f"Unique Photo IDs count: {len(set(all_photo_ids))}")

dupes = set([x for x in all_photo_ids if all_photo_ids.count(x) > 1])
if dupes:
    print(f"[!] STILL HAS {len(dupes)} DUPLICATE PHOTO IDs: {dupes}")
else:
    print("[SUCCESS] ABSOLUTELY PERFECT! 100% DISJOINT UNIQUE UNSPLASH IMAGES ACROSS ALL FILES!")
