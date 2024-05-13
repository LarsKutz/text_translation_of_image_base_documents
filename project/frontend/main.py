""" This module contains the main FastAPI application.
"""


import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uvicorn
import numpy as np
import cv2
import base64
import mimetypes
from backend.pipeline import Pipeline
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
pipeline = Pipeline()


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    """ Main page of the web application.

    Args:
        request (Request): The request object

    Returns:
        TemplateResponse: New HTML page
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def main(request: Request, src_language: str = Form(...), tgt_language: str = Form(...), file: UploadFile = File(...)):
    """ Main page of the web application. 

    Args:
        request (Request): The request object
        src_language (str, optional): Source Language from select-tag. Defaults to Form(...).
        tgt_language (str, optional): Target Language from select-tag. Defaults to Form(...).
        file (UploadFile, optional): File from input-tag. Defaults to File(...).

    Returns:
        TemplateResponse: New HTML page
    """
    
    try:
        img_bytes =  file.file.read()
        img = cv2.imdecode(np.fromstring(img_bytes, np.uint8), cv2.IMREAD_COLOR)  # BGR (Blue, Green, Red) format

        extracted_text, translated_text = pipeline.run(img, src_language, tgt_language)

        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        img_type = mimetypes.guess_type(file.filename)[0]

    except Exception as e:
        error_message_translation = f"An Error {type(e)} occured: {str(e)}!"
        return templates.TemplateResponse("index.html", {"request": request,
                                                            "error_message_translation": error_message_translation})

    return templates.TemplateResponse("index.html", {"request": request, 
                                                    "src_language": src_language, 
                                                    "tgt_language": tgt_language, 
                                                    "extracted_text": extracted_text,
                                                    "translated_text": translated_text,
                                                    "filename": truncateFileName(file.filename),
                                                    "img_base64": img_base64,
                                                    "img_type": img_type}) 



def truncateFileName(name: str, length: int=36) -> str:
    """ Truncate the file name.

    Args:
        name (str): The file name
        length (int, optional): The maximum length of the file name. Defaults to 36.

    Returns:
        str: The truncated file name
    """
    if len(name) >= length:
        name = name[:(length//4)] + "..." + name[-(length//4):]
    return name


if __name__ == '__main__':
    """ Run the FastAPI application.
    """
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
    