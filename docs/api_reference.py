# docs/api_reference.py

import os
import pkgutil
from pathlib import Path

import mkdocs_gen_files

package = "homematicip"
src_path = Path("src") / package
reference_path = Path("reference/python-api")

nav = mkdocs_gen_files.Nav()

for module_info in pkgutil.walk_packages([str(src_path)], prefix=f"{package}."):
    module_name = module_info.name
    file_name = module_name.replace(".", "/") + ".md"
    full_path = reference_path / file_name

    nav[module_name.split(".")] = full_path.as_posix()

    with mkdocs_gen_files.open(full_path, "w") as f:
        ident = module_name
        f.write(f"# `{ident}`\n\n::: {ident}\n")

    edit_path = Path("src") / (module_name.replace(".", "/") + ".py")
    mkdocs_gen_files.set_edit_path(full_path, edit_path)

with mkdocs_gen_files.open(reference_path / "index.md", "w") as f:
    f.write("# API Reference\n")

    for line in nav.build_literate_nav():
        f.write(line + "\n")
