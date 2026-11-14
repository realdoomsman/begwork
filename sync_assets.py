"""copy the begwork art into site/img/ and rewrite the memes/stickers/reactions lists in config.js.

run from anywhere:  python sync_assets.py
- begwork/memes/*.png       -> site/img/memes/
- begwork/stickers/*.png    -> site/img/stickers/
- begwork/reactions/*.(png|jpg|gif|webp) -> site/img/reactions/  (other people's begging memes)
- begwork/{main,pfp,banner}.png -> site/img/  (+ img/favicon.png, 64x64 from pfp.png)
images in img/memes, img/stickers and img/reactions that no longer exist in the source folder are removed,
so the site always matches the source folders.
"""
import re
import shutil
from pathlib import Path

SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
IMG = SITE / "img"
CONFIG = SITE / "config.js"


EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp")


def sync_folder(src: Path, dst: Path) -> list[str]:
    dst.mkdir(parents=True, exist_ok=True)
    names = sorted(p.name for p in src.iterdir() if p.suffix.lower() in EXTS) if src.is_dir() else []
    for n in names:
        shutil.copy2(src / n, dst / n)
    for old in dst.iterdir():
        if old.suffix.lower() in EXTS and old.name not in names:
            old.unlink()
    return [f"img/{dst.name}/{n}" for n in names]


def write_list(text: str, key: str, items: list[str], trailing_comma: bool) -> str:
    body = ",\n".join(f'    "{i}"' for i in items)
    value = f"[\n{body}\n  ]" if items else "[]"
    block = f"  // {key} start\n  {key}: {value}{',' if trailing_comma else ''}\n  // {key} end"
    pattern = re.compile(rf"  // {key} start\n.*?// {key} end", re.S)
    if not pattern.search(text):
        raise SystemExit(f"config.js: markers '// {key} start' / '// {key} end' missing")
    return pattern.sub(lambda _: block, text)


def main() -> None:
    IMG.mkdir(exist_ok=True)
    for name in ("main.png", "pfp.png", "banner.png"):
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, IMG / name)
        else:
            print(f"missing {src}")

    pfp = ROOT / "pfp.png"
    if pfp.exists():
        from PIL import Image

        with Image.open(pfp) as im:
            im.convert("RGB").resize((64, 64), Image.LANCZOS).save(IMG / "favicon.png")

    memes = sync_folder(ROOT / "memes", IMG / "memes")
    stickers = sync_folder(ROOT / "stickers", IMG / "stickers")
    reactions = sync_folder(ROOT / "reactions", IMG / "reactions")

    text = CONFIG.read_text(encoding="utf-8")
    text = write_list(text, "memes", memes, trailing_comma=True)
    text = write_list(text, "stickers", stickers, trailing_comma=True)
    text = write_list(text, "reactions", reactions, trailing_comma=False)
    CONFIG.write_text(text, encoding="utf-8", newline="\n")

    print(f"memes: {len(memes)}  stickers: {len(stickers)}  reactions: {len(reactions)}  -> {CONFIG}")


if __name__ == "__main__":
    main()
