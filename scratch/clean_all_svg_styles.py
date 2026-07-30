import os

ROOT = r"c:\Users\russe\Desktop\decorationShop"

old_style = "style=\"display:block;width:100%;height:100%;display:inline-block;width:14px;height:14px;vertical-align:middle;margin-right:4px\""
new_style = "style=\"display:inline-block;width:14px;height:14px;vertical-align:middle;margin-right:4px\""

count = 0
for root, dirs, files in os.walk(ROOT):
    if ".git" in root or "node_modules" in root or "scratch" in root:
        continue
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file_obj:
                content = file_obj.read()
            if old_style in content:
                content = content.replace(old_style, new_style)
                with open(filepath, 'w', encoding='utf-8') as file_obj:
                    file_obj.write(content)
                count += 1
                print(f"Fixed footer SVG style in {f}")

print(f"Done. Fixed {count} files.")
