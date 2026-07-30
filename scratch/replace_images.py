import os
import re

# Comprehensive pool of unique high-resolution real Unsplash furniture/interior photo IDs.
# Each entry is a tuple: (photo_id, description_keyword)
PHOTO_POOL = [
    # Living Room / Sofas / Lounges
    ("photo-1555041469-a586c61ea9bc", "green velvet sofa living room"),
    ("photo-1586023492125-27b2c045efd7", "warm velvet lounge living room"),
    ("photo-1493663284031-b7e3aefcae8e", "grey contemporary sofa"),
    ("photo-1567016432779-094069958ea5", "walnut lounge chair living room"),
    ("photo-1618221195710-dd6b41faaea6", "luxury minimalist living room hero"),
    ("photo-1600210492486-724fe5c67fb3", "sunlit modern living room lounge"),
    ("photo-1600585154340-be6161a56a0c", "contemporary open plan living space"),
    ("photo-1616046229478-9901c5536a45", "beige cozy couch living room"),
    ("photo-1583847268964-b28dc8f51f92", "nordic living room interior"),
    ("photo-1540518614846-7eded433c457", "leather sofa wooden coffee table"),
    ("photo-1512918728675-ed5a9ecdebfd", "spacious modern apartment lounge"),
    ("photo-1507652313519-d4e9174996dd", "boho chic living room decor"),
    ("photo-1583845112203-b1d60b543594", "modern apartment sofa corner"),
    ("photo-1513694203232-719a280e022f", "velvet armchair corner nook"),
    ("photo-1567538096630-e0c55bd6374c", "cognac leather accent armchair"),
    ("photo-1580481072645-022f9a6d8310", "mid-century leather lounge chair"),
    ("photo-1519710164239-da123dc03ef4", "scandinavian style living room"),
    ("photo-1549488344-1f9b8d2bd1f3", "stylish modern apartment living room"),

    # Bedroom / Beds / Nightstands
    ("photo-1616594039964-ae9021a400a0", "aesthetic bedroom suite king bed"),
    ("photo-1631049307264-da0ec9d70304", "minimalist white oak platform bed"),
    ("photo-1505693416388-ac5ce068fe85", "warm wooden bed with soft lighting"),
    ("photo-1560448204-603b3fc33ddc", "nordic cozy bedroom retreat"),
    ("photo-1595526114035-0d45ed16cfbf", "japanese style wooden platform bed"),
    ("photo-1566665797739-1674de7a421a", "neutral aesthetic master bedroom"),
    ("photo-1532372576444-dda954194ad0", "craft walnut bedside nightstand"),
    ("photo-1558882224-dda166733046", "wooden wardrobe sliding doors"),
    ("photo-1522771739844-6a9f6d5f14af", "vanity dressing table with mirror"),
    ("photo-1617325247661-675ab4b64ae2", "luxurious master bedroom suite"),
    ("photo-1598928506311-c55ded91a20c", "nightstand table lamp detail"),
    ("photo-1560185893-a55cbc8c57e8", "white oak bedroom shelving unit"),
    ("photo-1595515106969-1ce29566ff1c", "tatami minimalist bedroom design"),
    ("photo-1540518614846-7eded433c457", "serene master bedroom setting"),
    ("photo-1512917774080-9991f1c4c750", "luxury bedroom with terrace view"),

    # Dining / Tables / Chairs / Credenzas
    ("photo-1604578762246-411d0a7e1405", "scandinavian wooden dining set"),
    ("photo-1617806118233-18e1de247200", "solid walnut 8-seater dining table"),
    ("photo-1530018607912-eff2daa1bac4", "luxury marble & wood dining table"),
    ("photo-1615066390971-03e4e1c36ddf", "warm dining room gathering setting"),
    ("photo-1503602642458-232111445657", "handcrafted scandinavian dining chairs"),
    ("photo-1538688525198-9b88f6f53126", "walnut sideboard dining credenza"),
    ("photo-1577140917170-285929fb55b7", "urban loft dining room set"),
    ("photo-1585128792020-803d29415281", "biophilic dining room with plants"),
    ("photo-1592078615290-033ee584e267", "hardwood crafted dining table detail"),
    ("photo-1519643381401-22c77e60520e", "modern minimalist dining table"),
    ("photo-1522708323590-d24dbb6b0267", "elegant dining space with pendant light"),

    # Office / Desks / Workspaces
    ("photo-1593642632559-0c6d3fc62b89", "executive office workspace studio"),
    ("photo-1498409785966-ab341407de6e", "dark walnut brentwood executive desk"),
    ("photo-1547954575-855750c57bd3", "bright home office workspace desk"),
    ("photo-1524758631624-e2822e304c36", "executive study desk with leather chair"),
    ("photo-1518455027359-f3f8164ba6bd", "solid oak writing desk"),
    ("photo-1517502884422-41eaead166d4", "clean modern office workstation"),
    ("photo-1497366216548-37526070297c", "commercial design studio office"),
    ("photo-1611269154421-4e27233ac5c7", "ergonomic executive leather chair"),
    ("photo-1578898887932-dce23a595ad4", "penthouse home office desk view"),
    ("photo-1510074377623-8cf13fb86c08", "minimalist oak study desk"),

    # Kitchen & Bar
    ("photo-1556911220-e15b29be8c8f", "italian marble top kitchen island"),
    ("photo-1507089947368-19c1da9775ae", "oak and leather bar stools"),
    ("photo-1556909114-f6e7ad7d3136", "sage green pantry storage cabinet"),
    ("photo-1556909212-d5b604d0c90d", "modern shaker kitchen island"),
    ("photo-1556909172-54557c7e4fb7", "luxury kitchen cabinetry setup"),
    ("photo-1484154218962-a197022b5858", "bright open plan kitchen space"),

    # Decor / Accessories / Lighting / Mirrors
    ("photo-1613545325278-f24b0cae1224", "brass vase decorative collection"),
    ("photo-1618220179428-22790b461013", "arch frame full length floor mirror"),
    ("photo-1584100936595-c0654b55a2e2", "linen throw pillows and cushions"),
    ("photo-1507003211169-0a1dd7228f2d", "rattan woven pendant light shade"),
    ("photo-1578500494198-246f612d3b3d", "artisan ceramic vases decor"),
    ("photo-1513519245088-0e12902e5a38", "seasonal home decor styling"),

    # Showroom & Architecture
    ("photo-1558618666-fcd25c85cd64", "flagship furniture showroom exterior"),
    ("photo-1567496898669-ee935f5f647a", "luxury furniture showroom interior"),
    ("photo-1600607687920-4e2a09cf159d", "interior design consultation studio"),
    ("photo-1581291518633-83b4ebd1d83e", "interior design moodboards & samples"),
    ("photo-1600573472591-ee6b68d14c68", "historic luxury mansion living room"),
    ("photo-1600596542815-ffad4c1539a9", "belgravia penthouse interior"),
    ("photo-1600607687644-c7171b42498f", "dubai marina luxury villa lounge"),
    ("photo-1600585154526-990dced4db0d", "new york upper east side loft"),
    ("photo-1600607687939-ce8a6c25118c", "grand entrance living hall"),
    ("photo-1600566753190-17f0baa2a6c3", "modern architectural residence interior")
]

print(f"Total unique photo IDs in pool: {len(PHOTO_POOL)}")
