"""news-image-20261118 entry: copy the pre-rendered poster to /output/entry.png.

The poster (poster.png) is a newspaper-style editorial infographic summarizing
eight major world news stories from 18 November 2026. It was rendered once with
gen_poster.py; shipping the finished bytes keeps the run offline, deterministic
and instant.
"""

import os
import shutil

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poster.png")
    dst = os.path.join(OUTPUT_DIR, "entry.png")
    shutil.copyfile(src, dst)
    print(f"Copied {src} -> {dst}")

if __name__ == "__main__":
    main()
