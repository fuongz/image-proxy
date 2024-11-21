# Image Proxy - HEIC to PNG converter

## 🚀 Tech stack:

- FastAPI
- Pillow

## ✨ Features

- [x] Convert `.HEIC` to `.PNG`
- [x] Convert image to any file extensions
- [x] Resize image
- [ ] Support `.GIF` file

## ✅ Testing
```
https://api.phake.app/image/format(png):size(64:64)/https%3A%2F%2Fgithub.com%2Ftigranbs%2Ftest-heic-images%2Fraw%2Frefs%2Fheads%2Fmaster%2Fimage1.heic
```

## 🛠️ Development

1. Clone this repository

```
git clone git@github.com:fuongz/image-proxy.git
```

2. Install the required dependencies

```
# with venv
# python -m venv venv

pip install -r requirements.txt
```

3. Run with fastapi and expose to port 3000

```
fastapi dev app/main.py --port 3000
```

# License

- [MIT](./LICENSE)
