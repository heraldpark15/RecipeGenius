from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAIService:
    API_KEY = os.getenv("API_KEY")
    BASE_URL = os.getenv("BASE_URL")

    def __init__(self):
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key="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")

    def generate_recipe(self, chat_history, user_profile):
        # Unpack user_profile
        dietary_preference = user_profile.get("dietary_preference", None)
        allergies = user_profile.get("allergies", None)

        system_message_content = '''
                    "You are a recipe generator. Provide recipes in this format:\n"
                    "1. Title of the Dish\n2. List of ingredients\n3. Steps to prepare\n"
                    "4. Suggested Drink Pairing (with ingredients)"
                    "Do not include any reasoning, inner thoughts, or additional explanations. Only provide the recipe in the specified format. Avoid repeating recipes you've suggested earlier."
                    "If the user asks about content that is not related to recipe generation, please reply with 'Sorry, I am not equipped to answer questions unrelated to recipe generation'"
                '''
        
        if dietary_preference:
            system_message_content += f"\nUser prefers a {dietary_preference} diet. Please take this into account when suggesting recipes"
        if allergies:
            system_message_content += f"\nUser has the following allergies: {allergies}. Avoid including these ingredients in the recipe"
        
        system_message = {
            "role": "system",
            "content": system_message_content
        }

        messages = [system_message] + chat_history

        response = self.client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=messages
        )

        return response.choices[0].message.content