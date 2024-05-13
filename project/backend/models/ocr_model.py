""" This module contains the OCR model.
"""


import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import getpass
import pytesseract
import json
import cv2
from cv2.typing import MatLike
from utility.utility import get_path_to_language_shortcuts


""" Configuration of Tessaract:
tesseract --help-psm
    0     Orientation and script detection (OSD) only.
    1     Automatic page segmentation with OSD.
    2     Automatic page segmentation, but no OSD, or OCR. (not implemented)
    3     Fully automatic page segmentation, but no OSD. (Default)
    4     Assume a single column of text of variable sizes.
    5     Assume a single uniform block of vertically aligned text.
    6     Assume a single uniform block of text.
    7     Treat the image as a single text line.
    8     Treat the image as a single word.
    9     Treat the image as a single word in a circle.
    10    Treat the image as a single character.
    11    Sparse text. Find as much text as possible in no particular order.
    12    Sparse text with OSD.
    13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.

tesseract --help-oem
    0    Legacy engine only.
    1    Neural nets LSTM engine only.
    2    Legacy + LSTM engines.
    3    Default, based on what is available.
"""


class OCRModel:
    """ OCR model using Tesseract from Google.
    """

    def __init__(self, language="eng") -> None:
        """ Initialize the OCR model.

        Args:
            language (str, optional): The language of the text. Defaults to "eng".
        """
        with open(get_path_to_language_shortcuts(), "r") as file:
            self.__languages = json.load(file)
        self.__language = None
        self.__config = "--psm 3 --oem 3"
        
        self.set_language(language)

        # Path to tesseract.exe, change if necessary!      
        pytesseract.pytesseract.tesseract_cmd = os.path.join("C:\\Users", getpass.getuser(), r"AppData\Local\Programs\Tesseract-OCR" , "tesseract.exe")
    

    def set_language(self, language: str) -> None:
        """ Set the language of the text. Use language short code. 
        Available languages can be found in get_languages().

        Args:
            language (str): The language of the text.

        Raises:
            ValueError: If the language is not supported.
        """
        for shortcodes in self.__languages.values():
            if language in shortcodes.values():
                self.__language = language
                return
        raise ValueError(f"Language \"{language}\" not supported.")
        

    def get_language(self) -> str:
        """ Get the language of the text.

        Returns:
            str: The language of the text.
        """
        return self.__language
    

    def get_languages(self) -> dict:
        """ Get the available languages. 

        Returns:
            dict: The available languages.
        """
        return self.__languages
        

    def __preprocess_image(self, image: MatLike) -> MatLike:
        """ Preprocess an image.

        Args:
            image (MatLike): The input image.

        Returns:
            MatLike: The preprocessed image.
        """
        # Convert the image to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding
        image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        return image
    

    def extract_text(self, image: MatLike) -> str:
        """ Extract text from an image.

        Args:
            image (MatLike): The input image.

        Returns:
            str: The extracted text.
        """
        preprocessed_image = self.__preprocess_image(image)
        extracted_text = pytesseract.image_to_string(preprocessed_image, lang=self.__language, config=self.__config)
        return self.__postprocess_text(extracted_text)
    

    def __postprocess_text(self, extracted_text: str) -> str:
        """ Postprocess the extracted text. Remove next-line element and hyphens 
        at the end of a line and join the separated words together. 

        Args:
            extracted_text (str): The extracted text.

        Returns:
            str: The postprocessed text.
        """
        # Could use a LLM to correct the text
        return extracted_text


    def __str__(self) -> str:
        """ Get the model name.

        Returns:
            str: Model name.
        """
        return f"Tesseract version: {pytesseract.get_tesseract_version()}"
    