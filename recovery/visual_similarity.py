from PIL import Image
import numpy as np
import os


def extract_visual_features(image_path):
    """
    Extract simple visual features from an image.
    """

    image = Image.open(image_path).convert("RGB")

    # Resize every image to the same size
    image = image.resize((32, 32))

    pixels = np.array(image)

    # Average RGB color
    mean_color = pixels.mean(axis=(0, 1))

    # Color variation
    color_variation = pixels.std(axis=(0, 1))

    features = np.concatenate(
        [mean_color, color_variation]
    )

    return features


def calculate_similarity(features_a, features_b):
    """
    Calculate similarity between two images.
    """

    distance = np.linalg.norm(
        features_a - features_b
    )

    similarity = 100 / (1 + distance)

    return round(similarity, 2)


def compare_images(image_paths):
    """
    Compare every image with every other image.
    """

    results = []

    features = {}

    # Extract features
    for path in image_paths:

        try:

            features[path] = extract_visual_features(
                path
            )

        except Exception:

            pass


    # Compare images
    paths = list(features.keys())

    for i in range(len(paths)):

        for j in range(i + 1, len(paths)):

            image_a = paths[i]
            image_b = paths[j]

            similarity = calculate_similarity(
                features[image_a],
                features[image_b]
            )

            results.append({

                "image_a": os.path.basename(
                    image_a
                ),

                "image_b": os.path.basename(
                    image_b
                ),

                "similarity": similarity

            })


    return results