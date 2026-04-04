from pathlib import Path

import numpy as np
from PIL import Image, ImageOps


def load_and_prepare_image(image_path, target_size=(256, 256)):
    """Load an image, fix orientation, center-crop to square, and resize."""
    image_path = Path(image_path)
    with Image.open(image_path) as img:
        img = ImageOps.exif_transpose(img).convert("RGB")
        img = ImageOps.fit(img, target_size, method=Image.Resampling.LANCZOS)
        return np.array(img, dtype=np.float32)


def is_likely_fundus_image(image_array):
    """Heuristic check for retinal fundus-style images with dark corners."""
    gray = image_array.mean(axis=2)
    h, w = gray.shape
    corner_size_h = max(16, h // 8)
    corner_size_w = max(16, w // 8)

    corners = [
        gray[:corner_size_h, :corner_size_w],
        gray[:corner_size_h, -corner_size_w:],
        gray[-corner_size_h:, :corner_size_w],
        gray[-corner_size_h:, -corner_size_w:],
    ]
    corner_mean = float(np.mean([corner.mean() for corner in corners]))

    center = gray[h // 4: 3 * h // 4, w // 4: 3 * w // 4]
    center_mean = float(center.mean())

    return center_mean > 35 and (center_mean - corner_mean) > 25


def validate_fundus_image(image_array, image_path):
    if not is_likely_fundus_image(image_array):
        raise ValueError(
            f"{image_path} does not look like a retinal fundus image. "
            "These models were trained on retina/fundus photos, not regular mobile eye photos."
        )
