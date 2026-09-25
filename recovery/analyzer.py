from PIL import Image
import os


def analyze_file(file_path):

    result = {
        "file": os.path.basename(file_path),
        "size": os.path.getsize(file_path),
        "valid": False,
        "width": None,
        "height": None,
        "integrity_score": 0
    }

    try:
        with Image.open(file_path) as img:

            # Check whether Pillow can read the image
            img.verify()

        # Open again because verify() closes the image
        with Image.open(file_path) as img:

            result["width"], result["height"] = img.size
            result["valid"] = True
            result["integrity_score"] = 100

    except Exception:
        result["valid"] = False
        result["integrity_score"] = 0

    return result