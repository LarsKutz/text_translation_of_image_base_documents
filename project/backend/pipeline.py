""" This module controls the pipeline of the application.
"""


import json
from .models.ocr_model import OCRModel
from .models.translation_model import TranslationModel
from cv2.typing import MatLike
from .utility.utility import get_path_to_language_shortcuts


class Pipeline:
    """ Pipeline of the application.
    """

    def __init__(self) -> None:
        """ Initialize the pipeline.
        """
        with open(get_path_to_language_shortcuts(), "r") as file:
            self.__languages = json.load(file)
        self.__ocr = OCRModel()
        self.__translation = TranslationModel()


    def __change_language_to_shortcut(self, ocr: bool, language: str) -> str:
        """ Change the language to the shortcut. 

        Args:
            ocr (bool): True if the language is for OCR, False if it is for translation.
            language (str): Language to change.

        Returns:
            str: Shortcut of the language.
        """
        if ocr:
            return self.__languages[language]["tesseract"]
        return self.__languages[language]["translation"]


    def run(self, image: MatLike, src_language: str, tgt_language: str) -> tuple[str, str]:
        """ Run the pipeline. Translate the text from the image.

        Args:
            image (MatLike): Image to process.
            src_language (str): Source language.
            tgt_language (str): Target language.

        Returns:
            tuple[str, str]: Extracted Text, Translated text.
        """
        src_language_ocr = self.__change_language_to_shortcut(True, src_language)
        src_language_translation = self.__change_language_to_shortcut(False, src_language)
        tgt_language_translation = self.__change_language_to_shortcut(False, tgt_language)

        self.__ocr.set_language(src_language_ocr)
        self.__translation.set_languages(src_language_translation, tgt_language_translation)

        extracted_text = self.__ocr.extract_text(image)

        if not extracted_text:
            return "No Text found in the Image.", ""
        
        translated_text = self.__translation.translate(extracted_text)
        return extracted_text, translated_text
