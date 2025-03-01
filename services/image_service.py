import requests
from PIL import Image
from io import BytesIO
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

class ImageService:
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGING_TOKEN')}"}
    
    @staticmethod
    def generate_image(prompt):
        """Function to generate an image from Hugging Face API."""
        data = {"inputs": prompt}
        response = requests.post(ImageService.API_URL, headers=ImageService.HEADERS, json=data)
        
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image
        else:
            st.error("Error generating image. Please try again!")
            return None

        # try:
        #     response = requests.post(ImageService.API_URL, headers=ImageService.HEADERS, json=data)
        #     st.write(f"API Response Status Code: {response.status_code}")  # Log status code
        #     st.write(f"Response Headers: {response.headers}")  # Log headers

        #     if response.status_code == 200:
        #         return Image.open(BytesIO(response.content))
        #     else:
        #         st.error(f"Error generating image: {response.text}")  # Log error response
        #         return None
        # except requests.exceptions.RequestException as e:
        #     st.error(f"Request failed: {e}")  # Catch request errors
        #     return None