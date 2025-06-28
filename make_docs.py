import os
import yaml

SRC_PATH = "src/homematicip"
DOCS_PATH = "docs/reference/python-api"
MKDOCS_YML = "mkdocs.yml"
DOCS_ROOT = "docs"

os.makedirs(DOCS_PATH, exist_ok=True)

def is_module(filename):
    return filename.endswith(".py") and not filename.startswith("__")

def scan_md_files(base_dir):
    """
    Recursively scan for .md files and build a nested dict structure for nav.
    """
    nav = []
    entries = sorted(os.listdir(base_dir))
    for entry in entries:
        path = os.path.join(base_dir, entry)
        rel_path = os.path.relpath(path, DOCS_ROOT)
        if os.path.isdir(path):
            sub_nav = scan_md_files(path)
            if sub_nav:
                nav.append({entry: sub_nav})
        elif entry.endswith(".md"):
            title = os.path.splitext(entry)[0].replace("_", " ").replace("-", " ").title()
            nav.append({title: rel_path})
    return nav

modules = [f for f in os.listdir(SRC_PATH) if is_module(f)]

# Create a markdown file for each module
for module in modules:
    modulename = module[:-3]
    with open(os.path.join(DOCS_PATH, f"{modulename}.md"), "w") as f:
        f.write(f"# `{modulename}`\n\n")
        f.write(f"::: homematicip.{modulename}\n")

# Create an index file listing all modules
with open(os.path.join(DOCS_PATH, "index.md"), "w") as f:
    f.write("# Python API Reference\n\n")
    for module in modules:
        modulename = module[:-3]
        f.write(f"- [{modulename}]({modulename}.md)\n")

# Update mkdocs.yml nav
with open(MKDOCS_YML, "r") as f:
    mkdocs_cfg = yaml.safe_load(f)

mkdocs_cfg["nav"] = scan_md_files(DOCS_ROOT)

with open(MKDOCS_YML, "w") as f:
    yaml.dump(mkdocs_cfg, f, sort_keys=False, allow_unicode=True)
