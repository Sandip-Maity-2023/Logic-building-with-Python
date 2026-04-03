import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(disease):

    prompt = f"""
    Eye disease: {disease}

    Give:
    - description
    - severity
    - precautions
    - treatment suggestion
    """

    response = model.generate_content(prompt)

    return response.text