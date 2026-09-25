def generate_recovery_report(
    results,
    available_fragments,
    expected_fragments=None
):

    if not results:

        return {
            "status": "NOT RECOVERABLE",
            "best_score": 0,
            "best_order": [],
            "evidence": [],
            "available_fragments": available_fragments,
            "missing_fragments": 0
        }


    # Find the strongest reconstruction

    best_result = max(
        results,
        key=lambda result: result["recovery_score"]
    )


    best_score = best_result["recovery_score"]


    # Determine recovery status

    if best_score >= 90:

        status = "FULLY RECOVERABLE"

    elif best_score >= 50:

        status = "PARTIALLY RECOVERABLE"

    else:

        status = "LOW RECOVERY CONFIDENCE"


    # Determine missing fragments
    # only when expected count is known

    missing_fragments = None

    if expected_fragments is not None:

        missing_fragments = max(
            expected_fragments - available_fragments,
            0
        )


    # Return complete recovery intelligence

    return {

        "status": status,

        "best_score": best_score,

        "best_order": best_result["order"],

        "evidence": best_result.get(
            "evidence",
            []
        ),

        "available_fragments": available_fragments,

        "missing_fragments": missing_fragments
    }