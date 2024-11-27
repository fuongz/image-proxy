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

from app.utils.file import pretty_size

import requests

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

formatter = logging.Formatter("%(levelname)s:   %(asctime)s %(message)s")

console_handler.setFormatter(formatter)

MAX_FILE_SIZE = 12400000
SUPPORTED_FILE_TYPES = [
    "image/png",
    "image/jpeg",
    "image/heif",
    "image/heic",
    "image/webp",
]
SUPPORTED_OUTPUT_VIDEO_TYPES = ["JPG", "JPEG", "PNG", "WEBP"]

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
        "client_host": client_host,
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


@app.get("/{options}/{param:path}", name="path-convertor")
def proxy(request: Request):
    try:
        options, url = request.path_params.values()
        query_params = unquote(str(request.query_params))
        if query_params:
            url = f"{url}?{query_params}"
        decoded_url = unquote(url)
        options_dict = {}
        options_lts = options.split(":")
        for option in options_lts:
            option_key = option.split("(")[0]
            option_value = findall(r"\(.*?\)", option)
            if len(option_value) > 0:
                options_dict[option_key] = (
                    option_value[0].replace("(", "").replace(")", "")
                )
        if not decoded_url:
            return HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Unsupported media type. (Only support: {})".format(
                    ", ".join(SUPPORTED_FILE_TYPES)
                ),
            )

        resp = requests.head(decoded_url)

        if resp.headers.get("Content-Type", "") not in SUPPORTED_FILE_TYPES:
            return HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Unsupported media type. (Only support: {})".format(
                    ", ".join(SUPPORTED_FILE_TYPES)
                ),
            )

        if int(resp.headers.get("Content-length")) > int(MAX_FILE_SIZE):
            return HTTPException(
                status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                f"Max file size is {pretty_size(MAX_FILE_SIZE)}",
            )

        im = Image.open(requests.get(decoded_url, stream=True).raw)

        # Image format option
        image_format = (
            "PNG"
            if not options_dict.get("format")
            else options_dict.get("format").upper()
        )
        image_format = "JPEG" if image_format == "JPG" else image_format

        # Image quality
        image_quality = options_dict.get("quality", None)

        if image_format not in SUPPORTED_OUTPUT_VIDEO_TYPES:
            return HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Unsupported media type. (Only support: {})".format(
                    ", ".join(SUPPORTED_FILE_TYPES)
                ),
            )

        if im.format == "HEIF":
            img_response = image_to_byte_array(
                im, image_format, options_dict.get("size"), image_quality
            )
            media_type = f"image/{image_format.lower()}"
        elif im.format == "GIF":
            return HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY, "Unsupported media type"
            )
        else:
            img_response = image_to_byte_array(
                im, image_format, options_dict.get("size"), image_quality
            )
            media_type = f"image/{im.format.lower() if not image_format else image_format.lower()}"
        return Response(content=img_response, media_type=media_type)

    except Exception as e:
        logger.warning(e)
        return HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(e))


def image_to_byte_array(
    image: Image, image_format=None, size=None, quality=None
) -> bytes:
    new_size = None
    if size and "," in size:
        new_size = size.split(",")
    img_byte_arr = io.BytesIO()
    if new_size:
        image.thumbnail([int(new_size[0]), int(new_size[1])], Image.Resampling.LANCZOS)

    optimize_value = False
    quality_value = 75
    if image_format == "WEBP":
        quality_value = int(quality) if quality else 75
        optimize_value = True

    image.save(
        img_byte_arr,
        format=image.format if not image_format else image_format,
        quality=quality_value,
        optimize=optimize_value,
    )
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr
