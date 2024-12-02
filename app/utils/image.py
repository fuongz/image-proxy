from PIL import Image
import io


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
