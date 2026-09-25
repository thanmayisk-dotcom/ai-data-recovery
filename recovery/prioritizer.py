def prioritize_recovery(results):
    """
    Rank recovery candidates from strongest
    to weakest based on recovery score.
    """

    prioritized = sorted(
        results,
        key=lambda result: result["recovery_score"],
        reverse=True
    )

    for rank, result in enumerate(
        prioritized,
        start=1
    ):
        result["priority"] = rank

    return prioritized