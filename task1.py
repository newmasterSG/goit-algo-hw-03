import argparse
import sys
import shutil
from pathlib import Path


DEFAULT_IGNORE = {".git", "__pycache__", ".venv"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursively copy files from a source directory into a destination directory, "
                    "grouping them by extension."
    )
    parser.add_argument(
        "src",
        type=Path,
        help="Path to the source directory"
    )
    parser.add_argument(
        "dst",
        nargs="?",
        type=Path,
        default=Path("dist"),
        help="Path to the destination directory (default: ./dist)"
    )
    return parser.parse_args()


def children(dir_path: Path):
    items = []
    for p in dir_path.iterdir():
        if p.name in DEFAULT_IGNORE:
            continue
        items.append(p)
    return sorted(items, key=lambda x: (x.is_file(), x.name.lower()))


def walk(dir_path: Path):
    try:
        entries = children(dir_path)
    except PermissionError as ex:
        print(f"Access denied to directory: {dir_path} ({ex})", file=sys.stderr)
        return
    except OSError as ex:
        print(f"Failed to read directory: {dir_path} ({ex})", file=sys.stderr)
        return

    for entry in entries:
        if entry.is_dir():
            yield from walk(entry)
        elif entry.is_file():
            yield entry
        else:
            print(f"Skipping unknown filesystem object: {entry}", file=sys.stderr)


def copy_files(src_root: Path, dst_root: Path):
    src_root = src_root.resolve()
    dst_root = dst_root.resolve()

    if not src_root.exists():
        print(f"Source directory does not exist: {src_root}", file=sys.stderr)
        return

    if not src_root.is_dir():
        print(f"Source path is not a directory: {src_root}", file=sys.stderr)
        return

    try:
        dst_root.mkdir(parents=True, exist_ok=True)
    except OSError as ex:
        print(f"Failed to create destination directory {dst_root}: {ex}", file=sys.stderr)
        return

    for file_path in walk(src_root):
        ext = file_path.suffix.lower().lstrip(".")
        if not ext:
            ext = "no_ext"

        target_dir = dst_root / ext

        try:
            target_dir.mkdir(parents=True, exist_ok=True)
        except OSError as ex:
            print(f"Failed to create subdirectory {target_dir}: {ex}", file=sys.stderr)
            continue

        target_file = target_dir / file_path.name

        try:
            shutil.copy2(file_path, target_file)
        except PermissionError as ex:
            print(f"Access denied to file: {file_path} ({ex})", file=sys.stderr)
        except OSError as ex:
            print(f"Failed to copy {file_path} -> {target_file}: {ex}", file=sys.stderr)


def main():
    args = parse_args()
    copy_files(args.src, args.dst)


if __name__ == "__main__":
    main()
