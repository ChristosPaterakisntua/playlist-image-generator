from __future__ import annotations

import re


def sanitize_filename(filename: str, replacement: str = "_") -> str:
    """
    Sanitizes a filename so that it can safely be used on Windows.

    Invalid Windows filename characters are replaced with ``replacement``.
    Leading/trailing whitespace and periods are removed, and reserved
    Windows filenames are handled.

    Parameters
    ----------
    filename : str
        Original filename or filename stem.
    replacement : str, default "_"
        String used to replace invalid characters.

    Returns
    -------
    str
        A sanitized filename.

    Raises
    ------
    ValueError
        If ``filename`` is empty or contains no valid characters.
    """
    filename = filename.strip()

    if not filename:
        raise ValueError("Filename cannot be empty.")

    # Characters not allowed in Windows filenames:
    # < > : " / \ | ? *
    filename = re.sub(r'[<>:"/\\|?*]', replacement, filename)

    # Remove trailing spaces and periods.
    filename = filename.rstrip(" .")

    # Windows reserved filenames.
    reserved_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }

    if filename.upper() in reserved_names:
        filename = f"{filename}{replacement}"

    if not filename:
        raise ValueError("Filename contains no valid characters.")

    return filename


def ask_yes_or_no(prompt: str) -> bool:
    """
    Expects `y` or `n` as an input answer. If the answer is not valid the user is prompted again. 
    """
    prompt += " (y/n) "
    while True:
        ans = input(prompt).strip().lower()
        if ans in {"y", "n"}:
            return ans == "y"