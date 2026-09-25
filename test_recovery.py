from recovery.reconstruction import create_fragments, reconstruct_file

input_file = "data/damaged/IMG_4903.JPG"
fragment_folder = "data/damaged/fragments"
output_file = "data/recovered/IMG_4903_RECOVERED.JPG"

# Step 1: Split the image into fragments
fragments = create_fragments(
    input_file,
    fragment_folder,
    3
)

print("Created fragments:")
for fragment in fragments:
    print(fragment)

# Step 2: Reconstruct the image
reconstruct_file(
    fragments,
    output_file
)

print("\nRecovered file:")
print(output_file)