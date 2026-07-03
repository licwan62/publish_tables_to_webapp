from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"

PRIMARY_PAGES = [
    "index.html",
    "size-chart.html",
    "size-charts.html",
    "size-ref.html",
]


def copy_tree(source: Path, target: Path) -> None:
    if not source.exists():
        return
    shutil.copytree(source, target, dirs_exist_ok=True)


def copy_file(source: Path, target: Path) -> None:
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    copy_tree(ROOT / "assets", SITE / "assets")
    copy_tree(ROOT / "config", SITE / "config")
    copy_tree(ROOT / "data" / "generated", SITE / "data" / "generated")
    copy_tree(ROOT / "data" / "source" / "html", SITE / "data" / "source" / "html")

    for page in PRIMARY_PAGES:
        copy_file(ROOT / "pages" / "level-1" / page, SITE / page)

    copy_file(ROOT / "README.md", SITE / "README.md")
    copy_file(ROOT / ".nojekyll", SITE / ".nojekyll")


if __name__ == "__main__":
    main()
