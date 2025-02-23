import requests
from PIL import Image
from io import BytesIO
import streamlit as st

HUGGING_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"


headers = {"Authorization": f"Bearer {HUGGING_TOKEN}"}

def generate_image(prompt):
    """Function to generate an image from Hugging Face API."""
    data = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        st.error("Error generating image. Please try again!")
        return None