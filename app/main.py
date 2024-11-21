import io
import logging
from datetime import datetime
from re import findall
from time import time
from urllib.parse import unquote

from PIL import Image
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pillow_heif import register_heif_opener
import requests

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

formatter = logging.Formatter("%(levelname)s:   %(asctime)s %(message)s")

console_handler.setFormatter(formatter)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_heif_opener()

@app.middleware("http")
async def log_traffic(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    client_host = request.client.host
    log_params = {
        "request_method": request.method,
        "request_url": str(request.url),
        "request_size": request.headers.get("content-length"),
        "request_headers": dict(request.headers),
        "request_body": await request.body(),
        "response_status": response.status_code,
        "response_size": response.headers.get("content-length"),
        "response_headers": dict(response.headers),
        "process_time": process_time,
        "client_host": client_host
    }
    logger.warning(str(log_params))
    return response

@app.exception_handler(RequestValidationError)
async def standard_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "detail": "Missing required fields.",
            }
        ),
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    logger.warning("🚀 Exec time: {} sec".format(time() - start_time))
    return response


@app.get(
    "/{options}/{param:path}", name="path-convertor"
)
def proxy(request: Request):
    try:
        options, url = request.path_params.values()
        decoded_url = unquote(url)
        options_dict = {}
        options_lts = options.split(":")
        for option in options_lts:
            option_key = option.split("(")[0]
            option_value = findall(r'\(.*?\)', option)
            if len(option_value) > 0:
                options_dict[option_key] = option_value[0].replace("(", "").replace(")", "")
        if not decoded_url:
            return HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Unsupported media type")
        im = Image.open(requests.get(decoded_url, stream=True).raw)
        if im.format == "HEIF":
            image_format = "PNG" if not options_dict.get("format") else options_dict.get("format").upper()
            img_response = image_to_byte_array(im, image_format, options_dict.get("size"))
            media_type = f"image/{image_format.lower()}"
        elif im.format == "GIF":
            return HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY, "Unsupported media type"
            )
        else:
            image_format = None if not options_dict.get("format") else options_dict.get("format").upper()
            img_response = image_to_byte_array(im, image_format, options_dict.get("size"))
            media_type = f"image/{im.format.lower() if not image_format else image_format.lower()}"
        return Response(content=img_response, media_type=media_type)

    except Exception as e:
        logger.error(e)
        return HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid URL")


def image_to_byte_array(image: Image, image_format=None, size=None) -> bytes:
    new_size = None
    if size and "," in size:
        new_size = size.split(",")
    img_byte_arr = io.BytesIO()
    if new_size:
        image.thumbnail([int(new_size[0]), int(new_size[1])], Image.Resampling.LANCZOS)
    image.save(img_byte_arr, format=image.format if not image_format else image_format)
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr
