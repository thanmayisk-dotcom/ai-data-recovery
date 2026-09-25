from recovery.candidate_recovery import test_fragment_orders
from recovery.prioritizer import prioritize_recovery


fragment_folder = "data/damaged/fragments"
output_folder = "data/recovered/candidates"


results = test_fragment_orders(
    fragment_folder,
    output_folder
)


prioritized_results = prioritize_recovery(results)


print("\nRECOVERY PRIORITY")
print("-----------------")


for result in prioritized_results:

    print("\nPriority:", result["priority"])

    print("Order:")
    print(" → ".join(result["order"]))

    print(
        "Recovery Score:",
        result["recovery_score"],
        "/ 100"
    )