import os
from pathlib import Path
import calendar

# --- CONFIG ---
FOLDER = r"E:/Scanner/STATIONS/MANSA 2011"   # change this to your folder path
STATION = "MANSA002-MOZ304A"
YEAR = 2011
OBS_TIME = "06"               # time the observation happened
# ---------------

def rename_images(folder, station, year, obs_time):
    folder = Path(folder)

    # Get all image files sorted by name (ensuring correct order)
    images = sorted(folder.glob("*.*"))

    if len(images) != 12:
        print(f"❌ Error: Expected 12 images, found {len(images)}")
        return

    for month in range(1, 13):
        img_path = images[month - 1]

        # Get number of days in that month
        days_in_month = calendar.monthrange(year, month)[1]

        # Build new name
        new_name = f"{station}-{year}{month:02d}{days_in_month:02d}{obs_time}{img_path.suffix}"

        # Full output path
        new_path = folder / new_name

        # Rename
        img_path.rename(new_path)

        print(f"Renamed → {img_path.name}  →  {new_name}")

    print("\n✅ DONE — All 12 images renamed successfully!")

print(os.listdir(r"E:/Scanner/STATIONS/MANSA 2011 Missing 01,07,11"))

rename_images(FOLDER, STATION, YEAR, OBS_TIME)


