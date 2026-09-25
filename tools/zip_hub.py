import zipfile
from pathlib import Path

# Paths setup
REPO_DIR = Path(".")
OUTPUT_ZIP = Path("LastWarDataHub_Package.zip")

# Extensions to include
ALLOWED_EXTENSIONS = {".txt", ".yml", ".yaml", ".py"}

# Folders or files to exclude from the upload
IGNORE_PATHS = {".git", "__pycache__", "node_modules", "venv"}


def package_repository():
    with zipfile.ZipFile(
        OUTPUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED
    ) as zip_out:
        for file_path in sorted(REPO_DIR.rglob("*")):
            # Skip directories and ignored paths
            if file_path.is_dir() or any(
                part in IGNORE_PATHS for part in file_path.parts
            ):
                continue

            # Skip the output zip file itself
            if file_path.resolve() == OUTPUT_ZIP.resolve():
                continue

            # Include targeted extensions
            if file_path.suffix.lower() in ALLOWED_EXTENSIONS:
                relative_path = file_path.relative_to(REPO_DIR)
                zip_out.write(file_path, arcname=relative_path)
                print(f"Archived: {relative_path}")

    print(f"\nSuccess! Created archive: {OUTPUT_ZIP.resolve()}")


if __name__ == "__main__":
    package_repository()