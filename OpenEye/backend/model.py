from __future__ import annotations

import os
from typing import Any

from transformers import pipeline

MODEL_ID = os.getenv("OPENEYE_MODEL_ID", "dima806/retinal-disease-classifier")

_classifier: Any | None = None


def _get_classifier():
    global _classifier

    if _classifier is None:
        try:
            _classifier = pipeline("image-classification", model=MODEL_ID)
        except Exception as exc:  # pragma: no cover - depends on local/network env
            raise RuntimeError(
                "The eye disease model could not be loaded. "
                "Ensure the model is available locally or that network access is allowed."
            ) from exc

    return _classifier


def predict(image):
    classifier = _get_classifier()
    return classifier(image)
