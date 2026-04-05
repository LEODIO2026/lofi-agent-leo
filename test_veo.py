import os
from google import genai
from google.genai import types

client = genai.Client()
with open("assets/branding/Neon_Blossom_Dynamic.png", "rb") as f:
    img_bytes = f.read()

try:
    print("Testing types.Image...")
    op = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt="test",
        image=types.Image(image_bytes=img_bytes, mime_type="image/png")
    )
    print("types.Image Success!")
except Exception as e:
    print("types.Image Error:", e)

try:
    print("\nTesting dict payload...")
    op = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt="test",
        image={"image_bytes": img_bytes, "mime_type": "image/png"}
    )
    print("dict payload Success!")
except Exception as e:
    print("dict payload Error:", e)
