import os
from PIL import Image


def check_jpeg(filepath):
    try:
        with Image.open(filepath) as image:
            image.verify()

        return {
            "valid": True,
            "score": 100,
            "evidence": [
                "JPEG image verified successfully"
            ]
        }

    except Exception:
        return {
            "valid": False,
            "score": 0,
            "evidence": [
                "JPEG verification failed"
            ]
        }


def check_png(filepath):
    try:
        with Image.open(filepath) as image:
            image.verify()

        return {
            "valid": True,
            "score": 100,
            "evidence": [
                "PNG image verified successfully"
            ]
        }

    except Exception:
        return {
            "valid": False,
            "score": 0,
            "evidence": [
                "PNG verification failed"
            ]
        }


def check_pdf(filepath):
    try:
        with open(filepath, "rb") as file:
            data = file.read()

        if not data.startswith(b"%PDF"):
            return {
                "valid": False,
                "score": 0,
                "evidence": [
                    "PDF header not detected"
                ]
            }

        score = 60
        evidence = [
            "PDF header detected"
        ]

        if b"%%EOF" in data:
            score += 40
            evidence.append(
                "PDF end marker detected"
            )

        return {
            "valid": True,
            "score": score,
            "evidence": evidence
        }

    except Exception:
        return {
            "valid": False,
            "score": 0,
            "evidence": [
                "PDF verification failed"
            ]
        }


def check_txt(filepath):
    try:
        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        if len(content.strip()) > 0:

            return {
                "valid": True,
                "score": 100,
                "evidence": [
                    "Text content successfully read"
                ]
            }

        return {
            "valid": False,
            "score": 20,
            "evidence": [
                "Text file is empty"
            ]
        }

    except Exception:
        return {
            "valid": False,
            "score": 0,
            "evidence": [
                "Text file could not be decoded"
            ]
        }


def check_file_integrity(filepath, file_type):

    if file_type == "JPEG":
        return check_jpeg(filepath)

    if file_type == "PNG":
        return check_png(filepath)

    if file_type == "PDF":
        return check_pdf(filepath)

    if file_type == "TXT":
        return check_txt(filepath)

    return {
        "valid": False,
        "score": 0,
        "evidence": [
            "Unsupported file type"
        ]
    }