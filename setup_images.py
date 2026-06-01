"""
Run this once to extract and organise all outfit images from Sty_Images.zip.
Usage: python setup_images.py

The script:
  1. Extracts Sty_Images.zip into a temp folder
  2. Copies images into static/images/<english|traditional>/<casual|formal|office|wedding>/
  3. Lowercases all folder names to match the database paths
"""
import os
import shutil
import zipfile

BASE_DIR   = os.path.dirname(__file__)
ZIP_PATH   = os.path.join(BASE_DIR, 'Sty_Images.zip')
STATIC_DIR = os.path.join(BASE_DIR, 'static', 'images')
TEMP_DIR   = os.path.join(BASE_DIR, '_tmp_images')

# Folder name normalisation: zip has mixed case
FOLDER_MAP = {
    'english':     'english',
    'traditional': 'traditional',
    'casual':      'casual',
    'formal':      'formal',
    'office':      'office',
    'wedding':     'wedding',
    'Formal':      'formal',
    'Office':      'office',
    'Wedding':     'wedding',
}


def setup():
    if not os.path.exists(ZIP_PATH):
        print(f"ERROR: {ZIP_PATH} not found. Place Sty_Images.zip in the project root.")
        return

    # Extract
    print("Extracting images...")
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        z.extractall(TEMP_DIR)

    # Walk the extracted tree and copy to static/images
    copied = 0
    for root, dirs, files in os.walk(TEMP_DIR):
        for fname in files:
            if fname.startswith('.') or not any(fname.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                continue
            src = os.path.join(root, fname)
            # Derive relative path from temp root
            rel = os.path.relpath(src, TEMP_DIR)
            parts = rel.replace('\\', '/').split('/')
            # parts[0] = "Sty Images", parts[1] = clothing type, parts[2] = occasion, parts[3] = filename
            if len(parts) < 4:
                continue
            _, clothing_raw, occasion_raw, filename = parts[0], parts[1], parts[2], parts[3]
            clothing = FOLDER_MAP.get(clothing_raw, clothing_raw.lower())
            occasion = FOLDER_MAP.get(occasion_raw, occasion_raw.lower())
            dest_dir = os.path.join(STATIC_DIR, clothing, occasion)
            os.makedirs(dest_dir, exist_ok=True)
            dest = os.path.join(dest_dir, filename)
            shutil.copy2(src, dest)
            copied += 1

    # Cleanup temp
    shutil.rmtree(TEMP_DIR)
    print(f"Done. {copied} images copied to static/images/")


if __name__ == '__main__':
    setup()
