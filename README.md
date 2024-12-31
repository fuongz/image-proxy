# Image Proxy - HEIC to PNG converter

[![codecov](https://codecov.io/gh/fuongz/image-proxy/graph/badge.svg?token=TCMC32T0BW)](https://codecov.io/gh/fuongz/image-proxy) ![Unit Test](https://github.com/fuongz/image-proxy/actions/workflows/run_test.yml/badge.svg) ![GitHub Release](https://img.shields.io/github/v/release/fuongz/image-proxy)

## Table of Contents

- [Tech Stack](#tech-stack)
- [Feature](#feature)
- [Environment variables](#environment-variables)
- [Demo](#demo)
- [Development](#development)
- [License](#license)

## Tech stack:

- FastAPI
- Pillow

## Features

- [x] Convert image to any file extensions
- [x] Resize image
- [x] Support Bypass CORS
- [ ] Support `.GIF` file

## Environment variables

```
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
```

## Development

1. Clone this repository

```sh
git clone git@github.com:fuongz/image-proxy.git
```

2. Install the required dependencies

```sh
# with venv
# python -m venv venv

pip install -r requirements.txt
```

3. Run with fastapi and expose to port 3000

```sh
fastapi dev app/main.py --port 3000
```

# License

- [MIT](./LICENSE)
