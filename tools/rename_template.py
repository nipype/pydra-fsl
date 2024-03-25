#!/usr/bin/env python3
import sys
import os
import re
import fnmatch
import functools
from pathlib import Path

PACKAGE_ROOT = Path(__file__).absolute().parent.parent


@functools.lru_cache()
def load_gitignore(repo):
    gitignore = repo / ".gitignore"
    ignore = [fnmatch.translate(".git/"), fnmatch.translate(Path(__file__).name)]
    if gitignore.exists():
        ignore.extend(
            fnmatch.translate(line.strip())
            for line in gitignore.read_text().splitlines()
            if line.strip() and not line[0] == "#"
        )
    return re.compile("|".join(ignore))


cmd, new_name, *_ = sys.argv

for root_, dirs, files in os.walk(PACKAGE_ROOT):
    ignore = load_gitignore(PACKAGE_ROOT).search
    for d in [d for d in dirs if ignore(f"{d}/")]:
        dirs.remove(d)
    for f in [f for f in files if ignore(f)]:
        files.remove(f)

    root = Path(root_)
    for src in list(dirs):
        if "fsl" in src:
            dst = src.replace("fsl", new_name)
            print(f"Renaming: {root / src} ->  {root / dst}")
            os.rename(root / src, root / dst)
            dirs.remove(src)
            dirs.append(dst)
    for fname in files:
        text = Path.read_text(root / fname)
        if "fsl" in text:
            print(f"Rewriting: {root / fname}")
            Path.write_text(root / fname, text.replace("fsl", new_name))
