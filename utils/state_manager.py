import streamlit as st
from utils.diet_profile import DietProfile

class StateManager:
    def __init__(self):
        if "profile" not in st.session_state:
            st.session_state["profile"] = {"dietary_preference": None, "allergies": []}
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "system", "content": "You are a recipe idea generator."}
            ]
        if "button_clicked" not in st.session_state:
            st.session_state["button_clicked"] = None
        
        if "initial_message_shown" not in st.session_state:
            st.session_state["initial_message_shown"] = False

        if "saved_recipe" not in st.session_state:
            st.session_state["saved_recipe"] = "Nothing Yet!"

        self.diet_profile = DietProfile(
            dietary_preference=st.session_state["profile"]["dietary_preference"],
            allergies=st.session_state["profile"]["allergies"]
        )
    
    @property
    def profile(self):
        return st.session_state["profile"]

    @property
    def messages(self):
        return st.session_state["messages"]

    @property
    def button_clicked(self):
        return st.session_state["button_clicked"]
    
    @property
    def saved_recipe(self):
        return st.session_state["saved_recipe"]

    def set_button_clicked(self, value):
        st.session_state["button_clicked"] = value

    def reset_button_clicked(self):
        st.session_state["button_clicked"] = None

    def add_message(self, role, content):
        st.session_state["messages"].append({"role": role, "content": content})

    def update_user_profile(self, dietary_preference, allergies):
        allergies = [a.lower().strip() for a in allergies.split(",")]
        if dietary_preference != "Select":
            st.session_state["profile"]["dietary_preference"] = dietary_preference
        if allergies:
            st.session_state["profile"]["allergies"] = allergies
        self.diet_profile.set_dietary_preference(dietary_preference)
        self.diet_profile.set_allergies(allergies)
    
    def check_allergies(self, user_ingredients):
        return self.diet_profile.find_allergen(user_ingredients)

    def check_diet(self, user_ingredients):
        return self.diet_profile.check_diet(user_ingredients)
    
    def show_initial_message(self):
        if not st.session_state["initial_message_shown"]:
            st.session_state["initial_message_shown"] = True
            initial_message = (
                "Hey friend! I'm here to help you plan your whole meal, "
                "from the ingredients to the drinks. Would you like to provide "
                "ingredients to use or an idea of what you want?"
            )
            st.session_state.messages.append({"role": "assistant", "content": initial_message})
            st.chat_message("assistant").write(initial_message)
    
    def add_saved_recipe(self, saved_recipe):
        if saved_recipe:
            if st.session_state["saved_recipe"] == "Nothing Yet!":
                st.session_state["saved_recipe"] = []
            st.session_state["saved_recipe"].append(saved_recipe)