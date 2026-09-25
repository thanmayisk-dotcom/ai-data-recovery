import os
import itertools
import tempfile
from PIL import Image


def read_fragment(fragment_path):
    with open(fragment_path, "rb") as file:
        return file.read()


def get_fragments(folder):
    fragments = []

    for filename in os.listdir(folder):
        if filename.endswith(".part"):
            path = os.path.join(folder, filename)
            fragments.append(path)

    return sorted(fragments)


def validate_jpeg_sequence(fragment_paths):
    """
    Combine fragments in the supplied order and evaluate
    whether the resulting sequence forms a valid JPEG.
    """

    data = b""

    for fragment_path in fragment_paths:
        data += read_fragment(fragment_path)

    score = 0
    evidence = []

    # Check JPEG header
    if data.startswith(b"\xff\xd8\xff"):
        score += 40
        evidence.append(
            "JPEG header detected at sequence start"
        )

    # Check JPEG end marker
    if data.endswith(b"\xff\xd9"):
        score += 40
        evidence.append(
            "JPEG end marker detected at sequence end"
        )

    # Perform actual JPEG verification
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".jpg"
        ) as temp_file:

            temp_file.write(data)
            temp_file.flush()

            with Image.open(temp_file.name) as image:
                image.verify()

        score += 20

        evidence.append(
            "Combined fragment sequence verified as a JPEG"
        )

    except Exception:

        evidence.append(
            "Combined fragment sequence failed JPEG verification"
        )

    return {
        "score": score,
        "evidence": evidence
    }


def analyze_relationships(folder):
    """
    Test every possible fragment ordering.

    Each ordering is evaluated using actual JPEG
    structural evidence.
    """

    fragments = get_fragments(folder)

    if len(fragments) < 2:
        return []

    relationships = []

    for order in itertools.permutations(fragments):

        analysis = validate_jpeg_sequence(order)

        relationships.append({
            "order": [
                os.path.basename(fragment)
                for fragment in order
            ],
            "score": analysis["score"],
            "evidence": analysis["evidence"]
        })

    return relationships


def suggest_order(fragment_folder):
    """
    Find the fragment ordering that produces
    the strongest JPEG reconstruction.
    """

    fragments = get_fragments(fragment_folder)

    if not fragments:
        return []

    if len(fragments) == 1:
        return fragments

    best_order = None
    best_score = -1

    for order in itertools.permutations(fragments):

        analysis = validate_jpeg_sequence(order)

        if analysis["score"] > best_score:
            best_score = analysis["score"]
            best_order = order

    return list(best_order)
