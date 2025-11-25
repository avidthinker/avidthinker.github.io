from pathlib import Path


def check_preview(config):
    """
    Throws if a markdown article lacks a `more block`.

    NOTE: `more blocks` are used to truncate article previews.
        Without it, the preview shows the whole article, which
        may confuse the reader.
        In particular, a preview lacks a header navigation tree.
    """
    files_to_fix: list[str] = []

    root = Path(".")
    num_articles = 0
    for p in (root / "docs/posts").glob("**/*.md"):
        if not p.is_file():
            continue

        num_articles += 1
        if "\n<!-- more -->" not in p.read_text(encoding="utf-8"):
            files_to_fix.append(str(p))

    if num_articles == 0:
        raise RuntimeError("No generators were run!")
    if files_to_fix:
        sep = "\n    "
        files = sep + sep.join(files_to_fix)
        raise RuntimeError("`\\n<!-- more -->` not found in:" + files)
