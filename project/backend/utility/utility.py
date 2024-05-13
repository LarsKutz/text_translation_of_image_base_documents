""" This module contains the utility functions.
"""


import os
import getpass


def get_path_to_language_shortcuts() -> str:
    """ Get the path to the language shortcuts.

    Returns:
        str: Path to the language shortcuts.
    """
    return os.path.join("C:\\Users", getpass.getuser(), r"Desktop\text_translation_of_image_base_documents\project\backend\utility", r"language_shortcuts.json")