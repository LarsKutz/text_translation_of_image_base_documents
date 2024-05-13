""" This module contains the translation model.
"""


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import torch 
from utility.utility import get_path_to_language_shortcuts
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer


class TranslationModel:
    """ Translation model using Hugging Face transformers.
    """

    def __init__(self, src_language="en", tgt_language="de") -> None:
        """ Initialize the translation model.

        Args:
            src_language (str, optional): Source Language. Defaults to "en".
            tgt_language (str, optional): Target Language. Defaults to "de".
        """
        with open(get_path_to_language_shortcuts(), "r") as file:
            self.__languages = json.load(file)
        self.__src_language = None
        self.__tgt_language = None
        self.__model_name = None
        self.__model = None
        self.__tokenizer = None
        self.__model_pipe = None
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.set_languages(src_language, tgt_language)
        if self.__src_language and self.__tgt_language:
            self.__init_model()
        

    def __init_model(self) -> None:
        """ Initialize the translation model.
        """
        try:
            self.__model_name = f"Helsinki-NLP/opus-mt-{self.__src_language}-{self.__tgt_language}"
            self.__model = AutoModelForSeq2SeqLM.from_pretrained(self.__model_name)
            self.__tokenizer = AutoTokenizer.from_pretrained(self.__model_name)
            self.__model_pipe = pipeline("text2text-generation", model=self.__model, tokenizer=self.__tokenizer, device=self.__device)
        except Exception as e:
            raise ValueError(f"Model {self.__model_name} not found. Please check the language codes.")
        

    def __check_language(self, language: str) -> str:
        """ Check if the language is supported.

        Args:
            language (str): The language code.

        Returns:
            str: The language code.
        
        Raises:
            ValueError: If the language is not supported.
        """
        for shortcodes in self.__languages.values():
            if language in shortcodes.values():
                return language
        raise ValueError(f"Language \"{language}\" not supported.")
        
    
    def set_languages(self, scr_language: str, tgt_language: str) -> None:
        """ Set the source and target languages for the translation model.

        Args:
            scr_language (str): Source language.
            tgt_language (str): Target language.

        Raises:
            ValueError: If the language is not supported.
        """
        self.__src_language = self.__check_language(scr_language)
        self.__tgt_language = self.__check_language(tgt_language)

        self.__init_model()


    def get_languages(self) -> tuple[str, str]:
        """ Get Source and Target languages.

        Returns:
            tuple: Source and Target languages.
        """
        return self.__src_language, self.__tgt_language
    

    def get_all_languages(self) -> dict:
        """ Get all supported languages.

        Returns:
            dict: All supported languages.
        """
        return self.__languages


    def __preprocess_text(self, text: str) -> str:
        """ Preprocess the text.

        Args:
            text (str): The input text.

        Returns:
            str: The preprocessed text.
        """
        # Could use a LLM to correct the text
        return text


    def translate(self, text: str) -> str:
        """ Translate the text.

        Args:
            text (str): The input text.

        Returns:
            str: The translated text.
        """
        preprocessed_text = self.__preprocess_text(text)
        translated_text = self.__model_pipe(preprocessed_text)[0]["generated_text"]
        return self.__postprocess_text(translated_text)
    

    def __postprocess_text(self, text: str) -> str:
        """ Postprocess the text.

        Args:
            text (str): The input text.

        Returns:
            str: The postprocessed text.
        """
        # Could use a LLM to correct the text
        return text

    
    def __str__(self) -> str:
        """ Return the translation model as string.
        """
        return self.__model_name if self.__model_name else "No model initialized."
    