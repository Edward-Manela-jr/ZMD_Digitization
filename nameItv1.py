from pathlib import Path
import calendar
import re

# ================= CONFIG =================
BASE_DIR = r"D:/Day 4/Zambezi/zambezi"   # Folder that contains "Zambezi 2017", etc.
STATION = "ZAMBEZI01-MOZ304A"
OBS_TIME = "06"

DRY_RUN = input("Dry run? (True/False): ").lower() == "true"        # ⚠️ True = preview only | False = actually rename
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
# =========================================


def extract_year(name):
    """Extract a 4-digit year from folder name"""
    match = re.search(r"(19|20)\d{2}", name)
    return int(match.group(0)) if match else None


def rename_in_year_folder(year_folder: Path):
    year = extract_year(year_folder.name)
    if not year:
        print(f"⚠ Skipping (no year found): {year_folder.name}")
        return

    files = sorted(
        [f for f in year_folder.iterdir()
         if f.is_file() and f.suffix.lower() in ALLOWED_EXTS]
    )

    if not files:
        print(f"⚠ No image files in {year_folder.name}")
        return

    if len(files) > 12:
        print(f"⚠ WARNING: {year_folder.name} has {len(files)} files (expected max 12)")

    print(f"\n📂 Processing: {year_folder.name}")
    print(f"   Year detected: {year}")
    print(f"   Files found: {len(files)}")

    for idx, file in enumerate(files, start=1):
        if idx > 12:
            print("❌ More than 12 files — stopping")
            break

        month = idx
        days = calendar.monthrange(year, month)[1]
        new_name = f"{STATION}-{year}{month:02d}{days:02d}{OBS_TIME}{file.suffix}"
        new_path = year_folder / new_name

        if new_path.exists():
            print(f"⚠ Exists, skipped: {new_name}")
            continue

        if DRY_RUN:
            print(f"[DRY-RUN] {file.name} → {new_name}")
        else:
            file.rename(new_path)
            print(f"Renamed → {file.name} → {new_name}")


def process_all_year_folders(base_dir):
    base_dir = Path(base_dir)

    if not base_dir.exists():
        print("❌ Base directory does not exist!")
        return

    year_folders = [f for f in base_dir.iterdir() if f.is_dir()]

    if not year_folders:
        print("❌ No year folders found!")
        return

    print(f"🔍 Found {len(year_folders)} year folders")

    for folder in year_folders:
        rename_in_year_folder(folder)

    print("\n✅ DONE — Processing complete!")


process_all_year_folders(BASE_DIR)
