# text_translation_of_image_base_documents
The project enables the automatic translation of image-based documents into various language. 

## Intro
This project was my first major project involving AI models. 

This project arose from an idea to translate larger image-based texts into my own language in order to better understand the content and meaning of the text and to avoid misunderstandings.  

Therefore, because it is my first major project, it is not inevitable that everything will work. 

For this project i use [Tesseract](https://github.com/tesseract-ocr/tesseract) for text extraction and multiple models from [HuggingFace Helsinki-NLP](https://huggingface.co/Helsinki-NLP) for text translation.

## Contents
* [Feature overview](#feature-overview)
* [Requirements](#requirements)
* [Installation](#installation)
* [Add more languages](#add-more-languages)
* [Getting started](#getting-started)
    * [Setup](#setup)
    * [Usage](#usage)
* [License](#license)


## Feature overview
*   [x] Extracting text from images
*   [x] Translating text 
*   [x] Supporting different languages 

## Requirements
* [Tesseract 5.x.x](https://tesseract-ocr.github.io/tessdoc/Downloads.html)
* [Python 3.11.1+](https://www.python.org/downloads/release/python-3111/)
* [Pipenv](https://pypi.org/project/pipenv/) (optional)

Please install this requirements. `pipenv` is not necessary, but you have access to a virtual enviroment and its easier to install the necessary packages for this project.

## Installation 
Check installation with: 
```cmd
tesseract --version
```
```cmd
python --version
```
```cmd
pipenv --version
```

## Add more languages
You have to do a few changes in the following files:
* `project/frontend/templates/index.html`
* `project/backend/utility/language_shortcuts.json`

To have access to your new languages in the web browser you have to add two lines of code:
```html
<!-- index.html -->
<!-- Example adding Polish -->
<option value="polish" {{ "selected" if src_language == "polish" else "" }} >Polish</option>
```

The models also need to know the new languages. So we have to update the `language_shortcuts.json`-file. Just add following lines of code (example with polish). You need to know the shortcuts of the languages. You have access to shortcuts for [Tesseract here](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html) and for the [Translattion model here](https://huggingface.co/Helsinki-NLP):
```json
{
    "english": {
        "tesseract": "eng",
        "translation": "en"
    },
    "french": {
        "tesseract": "fra",
        "translation": "fr"
    },
    "german": {
        "tesseract": "deu",
        "translation": "de"
    },
    "spanish": {
        "tesseract": "spa",
        "translation": "es"
    },

    // Adding new language
    "polish": {
        "tesseract": "pol",
        "translation": "pl"
    }
}
```

Tesseract still dont know the new languages yet. You have to install the corresponding language package from [here](https://github.com/tesseract-ocr/tessdata). Just download the `xxx.traineddata` file for you  language and copy this to your Tesseract installation path in the existing folder `tessdata`.

The Translation model will automaticaly download the model for the translation if it is available on Huggingface. Therefore, certain directions may not work. You can watch [here](https://huggingface.co/Helsinki-NLP#models) to see which models are available.

## Changes that needs to be made

### Tesseract `.exe` path
You have to change the path in file `ocr_model.py` in line 59. You need your absolut path to your Tesseract OCR exe.

```python
pytesseract.pytesseract.tesseract_cmd = os.path.join("C:\\Users", getpass.getuser(), r"AppData\Local\Programs\Tesseract-OCR" , "tesseract.exe")
```

### `language_shortcuts.json` path
You have to change the apth in file `utility.py` in line 15. You need yout absolut paht to your `language_shortcuts.json`-file.

```python
return os.path.join("C:\\Users", getpass.getuser(), r"Desktop\text_translation_of_image_base_documents\project\backend\utility", r"language_shortcuts.json")
```

## Getting started

### Setup
To create the virtual environment, the necessary `Pipfiles` are already in the `project` folder.
Just navigate to `project/` and execute following command:
```cmd
pipenv install
``` 
All packages are being installed. You may need to reload your IDE to have access to your created environemnt.

### Usage
To start the application, navigate to `project/frontend` and execute following command:
```cmd
pipenv run py .\main.py
```
Now you started the application. To use the application in you web-browser, you have to know your ipv4-address. You can check it:
```cmd
ipconfig
```

Now go into your browser and pass follwing URL: `<your-ipv4-address>:8000`. Now you should see the application.
You can use the same URL to run the application on different devices.

## License
[MIT](https://choosealicense.com/licenses/mit/)