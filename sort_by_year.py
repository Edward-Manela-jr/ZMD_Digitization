from pathlib import Path
import re

# --- CONFIG ---
SOURCE_DIR = r"D:\Day 4\Zambezi\isoka"

STATION_NAME = "isoka"
# ----------------


def extract_year(filename):
    match = re.search(r"(19|20)\d{2}", filename)
    return match.group(0) if match else None



def sort_files_by_year(source_dir, station_name):
    source_dir = Path(source_dir)

    files = [f for f in source_dir.iterdir() if f.is_file()]

    if not files:
        print("❌ No files found!")
        return

    for file in files:
        year = extract_year(file.name)

        if not year:
            print(f"⚠ Skipped (no year found): {file.name}")
            continue

        year_folder = source_dir.parent / f"{station_name} {year}"
        year_folder.mkdir(exist_ok=True)

        destination = year_folder / file.name
        file.rename(destination)

        print(f"Moved → {file.name} → {year_folder.name}")

    print("\n✅ DONE — Files sorted by year!")


sort_files_by_year(SOURCE_DIR, STATION_NAME)
from pathlib import Path
import re

# --- CONFIG ---
SOURCE_DIR = r"D:\Day 4\Zambezi\zambezi"
STATION_NAME = "Zambezi"
# ----------------


def extract_year(filename):
    """Extract 4-digit year from filename"""
    match = re.search(r"\b(19|20)\d{2}\b", filename)
    return match.group(0) if match else None


def sort_files_by_year(source_dir, station_name):
    source_dir = Path(source_dir)

    files = [f for f in source_dir.iterdir() if f.is_file()]

    if not files:
        print("❌ No files found!")
        return

    for file in files:
        year = extract_year(file.name)

        if not year:
            print(f"⚠ Skipped (no year found): {file.name}")
            continue

        year_folder = source_dir.parent / f"{station_name} {year}"
        year_folder.mkdir(exist_ok=True)

        destination = year_folder / file.name
        file.rename(destination)

        print(f"Moved → {file.name} → {year_folder.name}")

    print("\n✅ DONE — Files sorted by year!")


sort_files_by_year(SOURCE_DIR, STATION_NAME)
