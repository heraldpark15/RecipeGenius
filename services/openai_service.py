from openai import OpenAI
from config import API_KEY, BASE_URL

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

    def generate_recipe(self, chat_history):
        system_message = {
            "role": "system",
            "content": "You are a recipe generator. Provide recipes in this format:\n"
                       "1. Title of the Dish\n2. List of ingredients\n3. Steps to prepare\n"
                       "4. Suggested Drink Pairing (with ingredients)"
                       "Do not include any reasoning, inner thoughts, or additional explanations. Only provide the recipe in the specified format. Avoid repeating recipes you've suggested earlier."
                       "If the user asks about content that is not related to recipe generation, please reply with 'Sorry, I am not equipped to answer questions unrelated to recipe generation'"
        }
        messages = [system_message] + chat_history

        response = self.client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=messages
        )

        return response.choices[0].message.content