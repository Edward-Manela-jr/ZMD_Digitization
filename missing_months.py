import os
from pathlib import Path
import calendar
import re

# --- CONFIG ---
FOLDER = r"E:/Scanner/STATIONS/MANSA 2010 Missing 01,07,11"
STATION = "MANSA002-MOZ304A"
OBS_TIME = "06"          # Time of observation
# ----------------


def parse_missing_months(folder_name):
    """
    Extract missing months from folder name.
    Example: "MANSA 2011 Missing 01,07,11"
    Returns: [1, 7, 11]
    """
    match = re.search(r"Missing (.*)", folder_name)
    if not match:
        return []  # No missing months stated
    
    nums = match.group(1).split(",")
    months = []
    for m in nums:
        m = m.strip()
        if m.isdigit():
            months.append(int(m))
    return months


def rename_images(folder, station, obs_time):
    folder = Path(folder)

    # Extract year from folder name
    year_match = re.search(r"\b(19|20)\d{2}\b", folder.name)
    if not year_match:
        print("❌ Could not detect year from folder name!")
        return

    year = int(year_match.group(0))

    # Detect missing months
    missing_months = parse_missing_months(folder.name)

    print(f"Detected missing months: {missing_months}")

    # Get available image files, sorted in correct order
    images = sorted(folder.glob("*.*"))

    expected_count = 12 - len(missing_months)

    if len(images) != expected_count:
        print(f"⚠ Warning: Expected {expected_count} images but found {len(images)}")
        print("Renaming based on available files...")
    
    img_index = 0

    for month in range(1, 13):
        if month in missing_months:
            print(f"Skipping missing month {month:02d}")
            continue

        if img_index >= len(images):
            print(f"❌ ERROR: Not enough images for month {month:02d}")
            break

        img_path = images[img_index]
        img_index += 1

        days_in_month = calendar.monthrange(year, month)[1]
        suffix = img_path.suffix

        # Build final name
        new_name = f"{station}-{year}{month:02d}{days_in_month:02d}{obs_time}{suffix}"
        new_path = folder / new_name

        img_path.rename(new_path)
        print(f"Renamed → {img_path.name}  →  {new_path.name}")

    print("\n✅ DONE — Images renamed successfully!")


rename_images(FOLDER, STATION, OBS_TIME)
