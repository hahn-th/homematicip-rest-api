"""Generate the API reference pages that mkdocstrings renders.

api-autonav did this, but it is an mkdocs plugin and the docs are built with
zensical, which does not run it. mkdocstrings itself works, so all that is
needed is one page per module holding its directive.
"""

import shutil
from pathlib import Path

SRC = Path("src/homematicip")
OUT = Path("docs/reference")


def module_paths() -> list[tuple[str, Path]]:
    """Return (dotted module name, output page) for every module."""
    pages = []
    for path in sorted(SRC.rglob("*.py")):
        if any(part.startswith("_") and part != "__init__.py" for part in path.parts):
            continue
        # Directories without __init__.py are namespace packages; griffe cannot
        # collect them, so mkdocstrings fails the build on their pages.
        if any(
            not (p / "__init__.py").exists()
            for p in path.parents
            if SRC in p.parents or p == SRC
        ):
            continue
        parts = list(path.relative_to(SRC.parent).parts)
        if parts[-1] == "__init__.py":
            parts.pop()
        else:
            parts[-1] = parts[-1].removesuffix(".py")
        if not parts:
            continue
        pages.append((".".join(parts), OUT.joinpath(*parts).with_suffix(".md")))
    return pages


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)

    pages = module_paths()
    for dotted, page in pages:
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(f"# {dotted}\n\n::: {dotted}\n", encoding="utf-8")

    index = ["# API reference", ""]
    for dotted, page in sorted(pages, key=lambda item: item[0]):
        index.append(f"- [{dotted}]({page.relative_to(OUT).as_posix()})")
    (OUT / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")

    print(f"generated {len(pages)} reference pages in {OUT}")


if __name__ == "__main__":
    main()
