import base64
import io
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


@app.get(
    "/",
)
def proxy(url: str):
    try:
        decoded_url = base64.b64decode(url)
        im = Image.open(requests.get(decoded_url, stream=True).raw)
        if im.format == "HEIF":
            converted_img = convert_heic(im)
            return Response(content=converted_img, media_type="image/png")

    except Exception:
        return HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid URL")


def convert_heic(im: Image, dest_type: str = "PNG"):
    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format=dest_type)
    return img_byte_arr.getvalue()
