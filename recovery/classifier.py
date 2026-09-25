from PIL import Image
import numpy as np
import os


def image_features(image_path):
    """
    Convert an image into a simple numerical feature vector.
    """

    image = Image.open(image_path).convert("RGB")
    image = image.resize((32, 32))

    pixels = np.array(image)

    # Average color of the image
    mean_color = pixels.mean(axis=(0, 1))

    # Standard deviation gives us some information
    # about how much the image varies
    color_variation = pixels.std(axis=(0, 1))

    features = np.concatenate([mean_color, color_variation])

    return features


def classify_images(image_paths):
    """
    Group visually similar images.
    """

    results = []

    for path in image_paths:

        try:
            features = image_features(path)

            results.append({
                "file": os.path.basename(path),
                "path": path,
                "features": features
            })

        except Exception:
            pass

    return results