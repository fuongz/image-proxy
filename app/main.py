import io
import logging
from datetime import datetime
from io import BytesIO
from re import findall
from urllib.parse import unquote, urlparse, quote
from starlette.exceptions import HTTPException as StarletteHTTPException

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
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

formatter = logging.Formatter("%(levelname)s:   %(asctime)s %(message)s")

console_handler.setFormatter(formatter)

# Constants
SUPPORTED_SCHEMES = ["http", "https"]
MAX_FILE_SIZE = 12400000
TIMEOUT = 15
SUPPORTED_FILE_TYPES = [
    "image/png",
    "image/jpeg",
    "image/heif",
    "image/heic",
    "image/webp",
]
SUPPORTED_OUTPUT_IMAGE_TYPES = ["JPG", "JPEG", "PNG", "WEBP"]

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


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(str(exc.detail))
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "status_code": exc.status_code,
                "detail": str(exc.detail),
            }
        ),
    )


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
    logger.info(str(log_params))
    return response


@app.exception_handler(RequestValidationError)
async def standard_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "detail": "Missing required fields.",
            }
        ),
    )


@app.get("/{options}/{param:path}", name="path-convertor")
def proxy(request: Request):
    options, url = request.path_params.values()
    query_params = quote(str(request.query_params))
    if query_params:
        url = f"{url}?{query_params}"
    decoded_url = unquote(url)
    options_dict = {}
    options_lts = options.split(":")
    for option in options_lts:
        option_key = option.split("(")[0]
        option_value = findall(r"\(.*?\)", option)
        if len(option_value) > 0:
            options_dict[option_key] = option_value[0].replace("(", "").replace(")", "")
    if not decoded_url:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Unsupported media type (1). (Only support: {})".format(
                ", ".join(SUPPORTED_FILE_TYPES)
            ),
        )

    # Parse URL
    parsed_url = urlparse(decoded_url)

    if parsed_url.scheme not in SUPPORTED_SCHEMES:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Unsupported scheme. (Only support: {})".format(
                ", ".join(SUPPORTED_SCHEMES)
            ),
        )

    resp = requests.get(
        decoded_url,
        headers={
            "origin": f"{parsed_url.scheme}://{parsed_url.hostname}",
            "referer": f"{parsed_url.scheme}://{parsed_url.hostname}",
            "User-Agent": request.headers.get("user-agent"),
        },
        timeout=TIMEOUT,
    )

    if resp.headers.get("Content-Type", "") not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Unsupported media type (2). (Only support: {})".format(
                ", ".join(SUPPORTED_FILE_TYPES)
            ),
        )

    content_length = resp.headers.get("Content-length")
    if not content_length:
        content_length = resp.headers.get("x-full-image-content-length")

    if not content_length:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"Can not detect file size, please try another image url!",
        )

    if int(content_length) > int(MAX_FILE_SIZE):
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"Max file size is {pretty_size(MAX_FILE_SIZE)}",
        )

    im = Image.open(BytesIO(resp.content))

    # Image format option
    image_format = (
        "PNG" if not options_dict.get("format") else options_dict.get("format").upper()
    )
    image_format = "JPEG" if image_format == "JPG" else image_format

    # Image quality
    image_quality = options_dict.get("quality", None)

    if image_format not in SUPPORTED_OUTPUT_IMAGE_TYPES:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Unsupported media type (3). (Only support: {})".format(
                ", ".join(SUPPORTED_FILE_TYPES)
            ),
        )

    if im.format == "HEIF":
        img_response = image_to_byte_array(
            im, image_format, options_dict.get("size"), image_quality
        )
        media_type = f"image/{image_format.lower()}"
    elif im.format == "GIF":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unsupported media type")
    else:
        img_response = image_to_byte_array(
            im, image_format, options_dict.get("size"), image_quality
        )
        media_type = (
            f"image/{im.format.lower() if not image_format else image_format.lower()}"
        )
    return Response(content=img_response, media_type=media_type)


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
