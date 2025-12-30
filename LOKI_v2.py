from pathlib import Path
import pytesseract
import cv2
import calendar
import re

# ================= CONFIG =================
BASE_DIR = r"D:/Day 4/Zambezi/zambezi"
STATION = "ZAMBEZI01-MOZ304A"
OBS_TIME = "06"

DRY_RUN = False        # 🔴 Set to True to simulate, False to rename
TEST_YEAR = 2011     # 🔒 ONLY this year will be processed

ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
# =========================================


def extract_year(folder_name):
    match = re.search(r"(19|20)\d{2}", folder_name)
    return int(match.group(0)) if match else None


def month_from_filename(name):
    match = re.search(r"(19|20)\d{2}(\d{2})\d{2}", name)
    if match:
        month = int(match.group(2))
        if 1 <= month <= 12:
            return month
    return None


def month_from_image(img_path):
    img = cv2.imread(str(img_path))
    if img is None:
        return None

    h, w, _ = img.shape

    # Wider & safer crop for MONTH column
    crop = img[
        int(h * 0.04):int(h * 0.25),
        int(w * 0.30):int(w * 0.70)
    ]

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 5
    )

    text = pytesseract.image_to_string(
        gray,
        config="--psm 6 -c tessedit_char_whitelist=0123456789"
    )

    numbers = re.findall(r"\d{1,2}", text)
    valid_months = [int(n) for n in numbers if 1 <= int(n) <= 12]

    # Require exactly ONE clear month
    if len(set(valid_months)) == 1:
        return valid_months[0]

    return None


def process_year_folder(folder):
    year = extract_year(folder.name)
    if year != TEST_YEAR:
        return

    files = [
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in ALLOWED_EXTS
    ]

    print(f"\n📂 {folder.name} ({len(files)} files)")

    for file in files:
        month = month_from_filename(file.name)
        source = "filename"

        if not month:
            month = month_from_image(file)
            source = "OCR"

        if not month:
            print(f"❌ Month unresolved: {file.name}")
            continue

        days = calendar.monthrange(year, month)[1]
        new_name = (
            f"{STATION}-{year}{month:02d}{days:02d}{OBS_TIME}{file.suffix}"
        )
        new_path = folder / new_name

        if new_path.exists():
            print(f"⚠ Exists, skipped: {new_name}")
            continue

        if DRY_RUN:
            print(f"[DRY-RUN:{source}] {file.name} → {new_name}")
        else:
            file.rename(new_path)
            print(f"Renamed ({source}) → {new_name}")


def run():
    base = Path(BASE_DIR)
    if not base.exists():
        print("❌ Base directory not found")
        return

    for folder in base.iterdir():
        if folder.is_dir():
            process_year_folder(folder)

    print("\n✅ DONE — SINGLE-YEAR OCR processing complete")


run()
