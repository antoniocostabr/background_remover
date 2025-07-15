from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, status
from dotenv import load_dotenv
from fastapi.security import APIKeyHeader
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
import numpy as np
import io
import os
from typing import Optional, Tuple

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def get_api_key_from_env():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise ValueError("API_KEY environment variable not set.")
    return api_key


BBox = Optional[Tuple[int, int, int, int]]  # (left, top, right, bottom)


def find_bbox(mask: Image.Image, threshold: int = 10) -> BBox:
    """Return bbox of all pixels with value > threshold in `mask`."""
    if mask.mode != "L":
        mask = mask.convert("L")

    arr = np.asarray(mask)
    visible = arr > threshold
    if not visible.any():
        return None

    rows = np.any(visible, axis=1)
    cols = np.any(visible, axis=0)

    top = rows.argmax()
    bottom = len(rows) - rows[::-1].argmax()        # exclusive
    left = cols.argmax()
    right = len(cols) - cols[::-1].argmax()         # exclusive

    return (left, top, right, bottom)


def center_object_on_bg(
    img: Image.Image,
    pad_pct: float,
    bg_color=(255, 255, 255),
    alpha_threshold: int = 10,
) -> Image.Image:
    """
    Crop transparent padding around `img`, add `pad_pct` uniform margin,
    and place the object on a new background of `bg_color`.
    """
    alpha = img.split()[-1]
    bbox = find_bbox(alpha, threshold=alpha_threshold)

    # Choose output mode based on bg_color length
    mode = "RGBA" if len(bg_color) == 4 else "RGB"

    if not bbox:  # fallback for fully‑transparent source
        canvas = Image.new(mode, img.size, bg_color)
        canvas.paste(img, (0, 0), img)
        return canvas

    fg = img.crop(bbox)
    obj_w, obj_h = fg.size
    pad_x = int(obj_w * pad_pct)
    pad_y = int(obj_h * pad_pct)

    canvas_w = obj_w + 2 * pad_x
    canvas_h = obj_h + 2 * pad_y
    canvas = Image.new(mode, (canvas_w, canvas_h), bg_color)
    canvas.paste(fg, (pad_x, pad_y), fg)
    return canvas


# ----------------------------------------------------------------------
# FastAPI config
# ----------------------------------------------------------------------
API_KEY = get_api_key_from_env()

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key")


async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )


# ----------------------------------------------------------------------
# Endpoints
# ----------------------------------------------------------------------
@app.post("/remove-background/", dependencies=[Depends(get_api_key)])
async def remove_background(
    file: UploadFile = File(...),
    filename: str = Form("background_removed.jpg"),
    add_white_background: bool = Form(True),
    centralize_object: bool = Form(True),
    foreground_thresh: int = Form(240),
    background_thresh: int = Form(10),
):
    # 1) Remove background
    input_image = await file.read()
    output_image_data = remove(input_image,
                               alpha_matting=True,
                               alpha_matting_foreground_threshold=foreground_thresh,
                               alpha_matting_background_threshold=background_thresh,
                               alpha_matting_erode_size=10 )

    # 2) Decide output format
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext in {".jpg", ".jpeg"}:
        save_format = "jpeg"
        media_type = "image/jpeg"
    elif ext == ".png":
        save_format = "png"
        media_type = "image/png"
    else:  # default → jpeg
        save_format = "jpeg"
        media_type = "image/jpeg"
        filename = f"{name}.jpg"
        ext = ".jpg"

    temp_file_path = os.path.join('temp', f"temp_processed_image{ext}")

    # 3) Load into PIL
    img = Image.open(io.BytesIO(output_image_data))
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Determine if we need a transparent background
    need_transparent_bg = (save_format == "png") and (not add_white_background)

    if centralize_object:
        if need_transparent_bg:
            processed = center_object_on_bg(
                img, 0.05, (0, 0, 0, 0)  # fully transparent background
            )
        elif add_white_background:
            processed = center_object_on_bg(img, 0.05, (255, 255, 255))
        else:  # black background for JPEG without white bg
            processed = center_object_on_bg(img, 0.05, (0, 0, 0))
    else:
        if add_white_background:
            processed = Image.new("RGB", img.size, (255, 255, 255))
            processed.paste(img, (0, 0), img)
        elif need_transparent_bg:
            processed = img
        else:  # black background for JPEG
            bg = Image.new("RGB", img.size, (0, 0, 0))
            bg.paste(img, (0, 0), img)
            processed = bg

    # 4) Save to disk
    if save_format == "png":
        processed.save(temp_file_path, "png")
    else:
        processed.convert("RGB").save(temp_file_path, "jpeg", quality=95)

    return FileResponse(temp_file_path, media_type=media_type, filename=filename)


@app.get("/")
def read_root():
    return {"message": "Welcome to the background removal API"}
