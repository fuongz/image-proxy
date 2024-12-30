import unittest
from io import BytesIO

from PIL import Image
from fastapi.testclient import TestClient
from fastapi import status

from app.main import app


class TestConvert(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.target_image_url = "https://static9.depositphotos.com/1431107/1154/i/450/depositphotos_11542091-stock-photo-sample-stamp.jpg"

    # def test_no_content_length_url(self):
    #     dirty_url = "https://scontent-fra3-1.cdninstagram.com/v/t51.29350-15/465209495_932741328757717_4905765761379356388_n.jpg?se=7&stp=dst-jpg_e35_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xNDQweDE4MDAuc2RyLmYyOTM1MC5kZWZhdWx0X2ltYWdlIn0&_nc_ht=scontent-fra3-1.cdninstagram.com&_nc_cat=101&_nc_ohc=nX_niCygskkQ7kNvgGxcX8e&_nc_gid=8d0a4d837a80403ca4f384d9e0d2da46&edm=ABmJApABAAAA&ccb=7-5&ig_cache_key=MzQ5MTUzNjk3NDA5ODYzMzY1Mw%3D%3D.3-ccb7-5&oh=00_AYC4aeI9wf7LQWkLJl6E-9Jatp4QQvnyYBimgmx_qnVT2w&oe=67524F27&_nc_sid=b41fef"
    #     response = self.client.get(f"/format(webp)/{dirty_url}")
    #     assert (
    #         response.status_code == 200
    #         and response.headers.get("content-type") == "image/webp"
    #     )

    def test_root(self):
        response = self.client.get("/")
        assert response.status_code == 404

    def test_convert_to_png(self):
        response = self.client.get(f"/format(png)/{self.target_image_url}")
        assert (
            response.status_code == 200
            and response.headers.get("content-type") == "image/png"
        )

    def test_convert_to_jpg(self):
        response = self.client.get(f"/format(jpg)/{self.target_image_url}")
        assert (
            response.status_code == 200
            and response.headers.get("content-type") == "image/jpeg"
        )

    def test_convert_to_webp(self):
        response = self.client.get(f"/format(webp)/{self.target_image_url}")
        assert (
            response.status_code == 200
            and response.headers.get("content-type") == "image/webp"
        )

    def test_convert_to_txt(self):
        response = self.client.get(f"/format(txt)/{self.target_image_url}")
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
            and response.content.decode("utf-8")
            == '{"status_code":400,"detail":"Unsupported media type (3). (Only support: image/png, image/jpeg, image/heif, image/heic, image/webp)"}'
        )

    def test_wrong_scheme(self):
        response = self.client.get(f"/format(png)/h{self.target_image_url}")
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
            and response.content.decode("utf-8")
            == '{"status_code":400,"detail":"Unsupported scheme. (Only support: http, https)"}'
        )

    def test_resize_to_200_200(self):
        response = self.client.get(
            f"/format(webp):size(200,200)/{self.target_image_url}",
        )
        im = Image.open(BytesIO(response.content))
        assert (
            response.status_code == 200
            and response.headers.get("content-type") == "image/webp"
            and im.width == 200
        )
