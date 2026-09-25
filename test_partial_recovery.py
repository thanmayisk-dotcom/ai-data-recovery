from recovery_report import generate_recovery_report
import os
import shutil

from recovery.candidate_recovery import test_fragment_orders


original_folder = "data/damaged/fragments"
partial_folder = "data/damaged/partial_fragments"
output_folder = "data/recovered/partial_candidates"


# Create a clean test folder
if os.path.exists(partial_folder):
    shutil.rmtree(partial_folder)

os.makedirs(partial_folder, exist_ok=True)


# Copy only TWO of the three fragments
shutil.copy(
    os.path.join(original_folder, "fragment_1.part"),
    partial_folder
)

shutil.copy(
    os.path.join(original_folder, "fragment_2.part"),
    partial_folder
)


print("\nPARTIAL RECOVERY TEST")
print("----------------------")

print("Available fragments:")

for filename in os.listdir(partial_folder):
    print("-", filename)


# Try recovery with the available fragments
results = test_fragment_orders(
    partial_folder,
    output_folder
)


print("\nRECOVERY CANDIDATES")
print("-------------------")

for result in results:

    print("\nOrder:")
    print(" → ".join(result["order"]))

    print(
        "Recovery Score:",
        result["recovery_score"],
        "/ 100"
    )


# Generate final recovery report
report = generate_recovery_report(
    results,
    available_fragments=2,
    expected_fragments=3
)


print("\nRECOVERY REPORT")
print("----------------")

print("Status:", report["status"])

print(
    "Best Recovery Score:",
    report["best_score"],
    "%"
)

print(
    "Best Order:",
    " → ".join(report["best_order"])
)

print(
    "Available Fragments:",
    report["available_fragments"]
)

print(
    "Missing Fragments:",
    report["missing_fragments"]
)