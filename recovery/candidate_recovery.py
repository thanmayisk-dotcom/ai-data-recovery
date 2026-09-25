import os
import itertools
import tempfile

from PIL import Image
from recovery.relationship import suggest_order


def read_fragment(fragment_path):
    with open(fragment_path, "rb") as file:
        return file.read()


def analyze_jpeg_data(data):
    """
    Analyze a reconstructed JPEG and produce
    an evidence-based recovery score.
    """

    score = 0
    evidence = []

    # JPEG Start Of Image marker
    if data.startswith(b"\xff\xd8"):
        score += 25
        evidence.append("JPEG header detected")

    # JPEG End Of Image marker
    if data.endswith(b"\xff\xd9"):
        score += 25
        evidence.append("JPEG end marker detected")

    # Try opening and verifying the JPEG
    try:

        with tempfile.NamedTemporaryFile(
            suffix=".jpg"
        ) as temp_file:

            temp_file.write(data)
            temp_file.flush()

            with Image.open(temp_file.name) as image:
                image.verify()

            score += 40
            evidence.append("Image successfully verified")

    except Exception:
        evidence.append("Image verification failed")

    # Basic size evidence
    if len(data) > 1000:
        score += 10
        evidence.append("Sufficient data size")

    return {
        "score": score,
        "evidence": evidence
    }


def create_candidate(
    fragment_order,
    output_folder,
    candidate_number
):

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    output_path = os.path.join(
        output_folder,
        f"candidate_{candidate_number}.jpg"
    )

    with open(
        output_path,
        "wb"
    ) as output_file:

        for fragment in fragment_order:

            output_file.write(
                read_fragment(fragment)
            )

    return output_path


def test_fragment_orders(
    fragment_folder,
    output_folder
):

    fragments = []

    for filename in os.listdir(
        fragment_folder
    ):

        if filename.endswith(".part"):

            fragments.append(
                os.path.join(
                    fragment_folder,
                    filename
                )
            )

    fragments = sorted(fragments)

    if not fragments:
        return []

    # ==================================================
    # INTELLIGENT FRAGMENT ORDER
    # ==================================================

    suggested_order = suggest_order(
        fragment_folder
    )

    # ==================================================
    # BUILD TEST ORDER LIST
    # ==================================================

    orders = []

    # Test the relationship engine's
    # suggested order first.
    if suggested_order:

        orders.append(
            tuple(suggested_order)
        )

    # Keep testing every possible
    # permutation for validation.
    for order in itertools.permutations(
        fragments
    ):

        if order not in orders:
            orders.append(order)

    # ==================================================
    # TEST CANDIDATES
    # ==================================================

    results = []

    for number, order in enumerate(
        orders,
        start=1
    ):

        candidate_path = create_candidate(
            order,
            output_folder,
            number
        )

        with open(
            candidate_path,
            "rb"
        ) as file:

            data = file.read()

        analysis = analyze_jpeg_data(
            data
        )

        evidence = analysis["evidence"].copy()

        # Add relationship-engine evidence
        if suggested_order:
            if list(order) == list(
                suggested_order
            ):

                evidence.append(
                    "Fragment order supported by relationship analysis"
                )

        results.append({

            "candidate": candidate_path,

            "order": [
                os.path.basename(fragment)
                for fragment in order
            ],

            "recovery_score": analysis["score"],

            "evidence": evidence

        })

    return results
