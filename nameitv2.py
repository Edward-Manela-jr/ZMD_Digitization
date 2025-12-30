from pathlib import Path
import calendar
import re

# ================= CONFIG =================
BASE_DIR = r"D:/Day 4/Zambezi/zambezi"
STATION = "ZAMBEZI01-MOZ304A"
OBS_TIME = "06"

DRY_RUN = True   # 🔴 Set to False when ready
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
# =========================================


def extract_year(name):
    match = re.search(r"(19|20)\d{2}", name)
    return int(match.group(0)) if match else None


def rename_in_year_folder(folder: Path):
    year = extract_year(folder.name)
    if not year:
        print(f"⚠ Skipping (no year): {folder.name}")
        return

    files = sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in ALLOWED_EXTS
    )

    total = len(files)
    if total == 0:
        print(f"⚠ No images in {folder.name}")
        return

    if total > 12:
        print(f"⚠ {folder.name}: {total} files (>12). Using last 12 only.")
        files = files[-12:]
        total = 12

    start_month = 13 - total

    print(f"\n📂 {folder.name}")
    print(f"   Year: {year}")
    print(f"   Files: {total}")
    print(f"   Month range assumed: {start_month:02d} → 12")

    for idx, file in enumerate(files):
        month = start_month + idx
        days = calendar.monthrange(year, month)[1]

        new_name = (
            f"{STATION}-{year}{month:02d}{days:02d}{OBS_TIME}{file.suffix}"
        )
        new_path = folder / new_name

        if new_path.exists():
            print(f"⚠ Exists, skipped: {new_name}")
            continue

        if DRY_RUN:
            print(f"[DRY-RUN] {file.name} → {new_name}")
        else:
            file.rename(new_path)
            print(f"Renamed → {file.name} → {new_name}")


def process_all(base_dir):
    base_dir = Path(base_dir)
    folders = [f for f in base_dir.iterdir() if f.is_dir()]

    print(f"🔍 Found {len(folders)} year folders")

    for folder in folders:
        rename_in_year_folder(folder)

    print("\n✅ DONE")


process_all(BASE_DIR)
