import os
from google import genai
from google.genai import types

client = genai.Client()
prompt = "A relaxing 1-minute lofi chillhop beat with soft piano."
try:
    response = client.models.generate_content(
        model="lyria-3-pro-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO", "TEXT"],
        ),
    )
    print("Response:", response)
    print("Parts:", response.parts)
    if not response.parts:
        print("Candidates:", response.candidates)
except Exception as e:
    print("Error:", e)
