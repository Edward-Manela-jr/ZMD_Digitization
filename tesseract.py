# # import pytesseract
# # from PIL import Image

# # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # print(pytesseract.get_tesseract_version())






# from pathlib import Path
# import pytesseract
# import cv2
# import calendar
# import re

# # ================= CONFIG =================
# BASE_DIR = r"D:/Day 4/Zambezi/zambezi"
# STATION = "ZAMBEZI01-MOZ304A"
# OBS_TIME = "06"

# DRY_RUN = True   # 🔴 Set to False when confident
# ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )
# # =========================================


# def extract_year(folder_name):
#     m = re.search(r"(19|20)\d{2}", folder_name)
#     return int(m.group(0)) if m else None


# def extract_month_from_image(img_path):
#     img = cv2.imread(str(img_path))
#     if img is None:
#         return None

#     h, w, _ = img.shape

#     # 🔍 Precise crop for MONTH box (based on your scan)
#     crop = img[
#         int(h * 0.05):int(h * 0.22),     # vertical slice
#         int(w * 0.35):int(w * 0.65)      # horizontal slice
#     ]

#     gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
#     gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
#     _, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#     text = pytesseract.image_to_string(
#         gray,
#         config="--psm 6 -c tessedit_char_whitelist=0123456789"
#     )

#     numbers = re.findall(r"\d{1,2}", text)
#     for n in numbers:
#         m = int(n)
#         if 1 <= m <= 12:
#             return m

#     return None


# def process_year_folder(folder):
#     year = extract_year(folder.name)
#     if not year:
#         print(f"⚠ No year in folder name: {folder.name}")
#         return

#     files = [
#         f for f in folder.iterdir()
#         if f.is_file() and f.suffix.lower() in ALLOWED_EXTS
#     ]

#     print(f"\n📂 {folder.name} ({len(files)} files)")

#     for file in files:
#         month = extract_month_from_image(file)

#         if not month:
#             print(f"❌ Month not detected: {file.name}")
#             continue

#         days = calendar.monthrange(year, month)[1]
#         new_name = (
#             f"{STATION}-{year}{month:02d}{days:02d}{OBS_TIME}{file.suffix}"
#         )
#         new_path = folder / new_name

#         if new_path.exists():
#             print(f"⚠ Exists, skipped: {new_name}")
#             continue

#         if DRY_RUN:
#             print(f"[DRY-RUN] {file.name} → {new_name}")
#         else:
#             file.rename(new_path)
#             print(f"Renamed → {file.name} → {new_name}")


# def run_all(base_dir):
#     for folder in Path(base_dir).iterdir():
#         if folder.is_dir():
#             process_year_folder(folder)

#     print("\n✅ DONE — OCR-based renaming complete")


# run_all(BASE_DIR)











#/////////////////////////////////////////////////////////

from pathlib import Path
import pytesseract
import cv2
import calendar
import re

# ================= CONFIG =================
BASE_DIR = r"D:/Day 4/Zambezi/zambezi"
STATION = "ZAMBEZI01-MOZ304A"
OBS_TIME = "06"

DRY_RUN = True   # 🔴 Change to False when confident
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
# =========================================


def extract_year(folder_name):
    m = re.search(r"(19|20)\d{2}", folder_name)
    return int(m.group(0)) if m else None


def month_from_filename(name):
    m = re.search(r"(19|20)\d{2}(\d{2})\d{2}", name)
    if m:
        month = int(m.group(2))
        if 1 <= month <= 12:
            return month
    return None


def month_from_image(img_path):
    img = cv2.imread(str(img_path))
    if img is None:
        return None

    h, w, _ = img.shape

    # 🔧 Wider, safer crop for MONTH box
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

    valid = [int(n) for n in numbers if 1 <= int(n) <= 12]

    # Require EXACTLY ONE clear month
    if len(set(valid)) == 1:
        return valid[0]

    return None


def process_year_folder(folder):
    year = extract_year(folder.name)
    if not year:
        print(f"⚠ No year in folder: {folder.name}")
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


def run_all():
    for folder in Path(BASE_DIR).iterdir():
        if folder.is_dir():
            process_year_folder(folder)

    print("\n✅ DONE — SAFE OCR processing complete")


run_all()
from pathlib import Path
import pytesseract
import cv2
import calendar
import re

# ================= CONFIG =================
BASE_DIR = r"D:/Day 4/Zambezi/zambezi"
STATION = "ZAMBEZI01-MOZ304A"
OBS_TIME = "06"

DRY_RUN = True   # 🔴 Change to False when confident
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
# =========================================


def extract_year(folder_name):
    m = re.search(r"(19|20)\d{2}", folder_name)
    return int(m.group(0)) if m else None


def month_from_filename(name):
    m = re.search(r"(19|20)\d{2}(\d{2})\d{2}", name)
    if m:
        month = int(m.group(2))
        if 1 <= month <= 12:
            return month
    return None


def month_from_image(img_path):
    img = cv2.imread(str(img_path))
    if img is None:
        return None

    h, w, _ = img.shape

    # 🔧 Wider, safer crop for MONTH box
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

    valid = [int(n) for n in numbers if 1 <= int(n) <= 12]

    # Require EXACTLY ONE clear month
    if len(set(valid)) == 1:
        return valid[0]

    return None


def process_year_folder(folder):
    year = extract_year(folder.name)
    if not year:
        print(f"⚠ No year in folder: {folder.name}")
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


def run_all():
    for folder in Path(BASE_DIR).iterdir():
        if folder.is_dir():
            process_year_folder(folder)

    print("\n✅ DONE — SAFE OCR processing complete")


run_all()
