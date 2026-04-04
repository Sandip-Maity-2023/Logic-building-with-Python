from __future__ import annotations

import os

import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("OPENEYE_GEMINI_MODEL", "gemini-1.5-flash")

_model = None


def _get_model():
    global _model

    if not GEMINI_API_KEY:
        return None

    if _model is None:
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel(GEMINI_MODEL)

    return _model


def generate_response(disease):
    prompt = f"""
    Eye disease: {disease}

    Give:
    - description
    - severity
    - precautions
    - treatment suggestion
    """

    model = _get_model()
    if model is None:
        return (
            "Detailed AI guidance is unavailable because GEMINI_API_KEY is not configured. "
            f"The detected condition was '{disease}'. Please consult an eye specialist for advice."
        )

    try:
        response = model.generate_content(prompt)
    except Exception as exc:  # pragma: no cover - external API behavior
        raise RuntimeError("Failed to generate the medical explanation from Gemini.") from exc

    return response.text
