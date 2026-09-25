import os


FILE_SIGNATURES = {
    "JPEG": b"\xFF\xD8\xFF",
    "PNG": b"\x89PNG",
    "PDF": b"%PDF",
}


def identify_file_type(filepath):

    with open(filepath, "rb") as file:
        header = file.read(8)

    for file_type, signature in FILE_SIGNATURES.items():

        if header.startswith(signature):
            return file_type

    # Text files usually don't have a fixed binary signature.
    # Use the file extension as an additional clue.

    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".txt":
        return "TXT"

    return "UNKNOWN"


def scan_directory(directory):

    results = []

    for filename in os.listdir(directory):

        filepath = os.path.join(
            directory,
            filename
        )

        if os.path.isfile(filepath):

            file_type = identify_file_type(
                filepath
            )

            size = os.path.getsize(
                filepath
            )

            results.append({

                "filename": filename,

                "type": file_type,

                "size": size,

                "path": filepath

            })

    return results