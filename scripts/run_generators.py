from pathlib import Path
import subprocess
import sys
import hashlib
import json


hashes_path = "generators_hashes.json"


def rindex[T](xs: list[T], value: T) -> int:
    return len(xs) - 1 - xs[::-1].index(value)


def load_hashes(fpath: Path | str) -> dict[str, str]:
    fpath = Path(fpath)
    if not fpath.exists():
        return {}
    with fpath.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_hashes(fpath: Path | str, hashes: dict[str, str]) -> None:
    fpath = Path(fpath)
    with fpath.open("w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2)


def file_hash(fpath: Path | str, algo: str = "sha256") -> str:
    fpath = Path(fpath)
    h = hashlib.new(algo)
    with fpath.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def run_generators(config):
    """
    Runs generators of assets (e.g. svg images) found in `__generators__`
    dirs and put the generated assets in the associated `__generated__`
    dirs.

    NOTE:
    * Generators have extension `.gen.py`.
      * If a generator has changed, it's rerun.
    * The other .py files are considered shared files.
      * If a shared file has changed, all generators are rerun.
    * Avoiding unneeded rerun is more efficient and also prevents `mkdocs serve`
      from getting stuck in a loop.
    * The hashes are in "<project_root>/generators_hashes.json".
    """
    hashes = load_hashes(hashes_path)
    new_hashes: dict[str, str] = {}

    root = Path(".")
    fps = (root / "docs/posts").glob("**/__generators__/**/*.py")
    fps = [p for p in fps if p.is_file()]

    # checks whether any shared file has changed
    rerun_all = False
    for p in fps:
        if p.name.endswith(".gen.py"):
            continue
        # p is a shared file
        hash = file_hash(p)
        new_hashes[str(p)] = hash
        if hashes.get(str(p)) != hash:
            rerun_all = True

    num_generators = 0
    for p in fps:
        if not p.name.endswith(".gen.py"):
            continue
        # p is a generator
        num_generators += 1

        # skips unchanged generators unless rerun_all is true
        hash = file_hash(p)
        new_hashes[str(p)] = hash
        if not rerun_all and hashes.get(str(p)) == hash:
            continue

        # runs generator `p` with the correct `__generated__` working directory

        # Replaces (the last) `__generators__` with `__generated__` and removes the
        # last part (the file name).
        parts = list(p.parts)
        gen_idx = rindex(parts, "__generators__")
        workdir = Path(*parts[:gen_idx], "__generated__", *parts[gen_idx + 1 : -1])
        workdir.mkdir(exist_ok=True, parents=True)

        try:
            subprocess.run(
                [sys.executable, str(p.resolve())],
                cwd=workdir,
                check=True,  # raises on fail
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Generator {p} failed with exit code {e.returncode}"
            ) from e

    save_hashes(hashes_path, new_hashes)

    if num_generators == 0:
        raise RuntimeError("No generators were run!")
