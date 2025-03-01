from openai import OpenAI
# from config import API_KEY, BASE_URL

API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"

class OpenAIService:
    def __init__(self):
        print(API_KEY)
        self.client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

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
            system_message_content += f"\nUser prefers a {dietary_preference} diet. Please mention this in your output"
        if allergies:
            system_message_content += f"\nUser has the following allergies: {allergies}. Please mention this in your output"
        
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