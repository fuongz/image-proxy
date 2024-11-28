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
