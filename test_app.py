
import io
from urllib.parse import urlencode

from app import app


def test_home_page():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"QRForge" in response.data


def test_generate_qr_form():
    response = app.test_client().post(
        "/", data={"text": "https://github.com"}
    )
    assert response.status_code == 200
    assert b"Your QR code is ready!" in response.data


def test_empty_input():
    response = app.test_client().post(
        "/", data={"text": ""}
    )
    assert response.status_code == 200
    assert b"Please enter some text" in response.data


def test_qr_image_generation():
    query = urlencode({"text": "Hello QRForge"})
    response = app.test_client().get(f"/qr-image?{query}")

    assert response.status_code == 200
    assert response.mimetype == "image/png"
    assert response.data.startswith(b"\x89PNG\r\n\x1a\n")


def test_invalid_qr_image():
    response = app.test_client().get("/qr-image")

    assert response.status_code == 400


def test_download_qr_image():
    query = urlencode({
        "text": "Hello QRForge",
        "download": "1"
    })
    response = app.test_client().get(f"/qr-image?{query}")

    assert response.status_code == 200
    assert "attachment" in response.headers.get(
        "Content-Disposition", ""
    )
