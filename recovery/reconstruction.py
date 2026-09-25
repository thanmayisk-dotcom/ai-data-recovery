import os


def create_fragments(filepath, output_folder, number_of_fragments=3):

    os.makedirs(output_folder, exist_ok=True)

    with open(filepath, "rb") as file:
        data = file.read()

    total_size = len(data)
    fragment_size = total_size // number_of_fragments

    fragments = []

    for i in range(number_of_fragments):

        start = i * fragment_size

        if i == number_of_fragments - 1:
            end = total_size
        else:
            end = (i + 1) * fragment_size

        fragment_data = data[start:end]

        fragment_name = f"fragment_{i + 1}.part"
        fragment_path = os.path.join(
            output_folder,
            fragment_name
        )

        with open(fragment_path, "wb") as fragment_file:
            fragment_file.write(fragment_data)

        fragments.append(fragment_path)

    return fragments
def reconstruct_file(fragment_paths, output_path):

    with open(output_path, "wb") as output_file:

        for fragment_path in fragment_paths:

            with open(fragment_path, "rb") as fragment_file:
                data = fragment_file.read()

            output_file.write(data)

    return output_path  