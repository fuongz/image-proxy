import base64
import io
from time import time
from PIL import Image
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pillow_heif import register_heif_opener
import requests

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
    print("🚀 Exec time: {} sec".format(time() - start_time))
    return response


@app.get(
    "/",
)
def proxy(url: str, f: str = None):
    try:
        decoded_url = base64.b64decode(url)
        im = Image.open(requests.get(decoded_url, stream=True).raw)
        if im.format == "HEIF":
            format = "PNG" if not f else f.upper()
            img_response = image_to_byte_array(im, format)
            media_type = f"image/{format.lower()}"
        elif im.format == "GIF":
            return HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY, "Unsupported media type"
            )
        else:
            format = None if not f else f.upper()
            img_response = image_to_byte_array(im, format)
            media_type = f"image/{im.format.lower() if not format else format.lower()}"
        return Response(content=img_response, media_type=media_type)

    except Exception:
        return HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid URL")


def image_to_byte_array(image: Image, format=None) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format if not format else format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
