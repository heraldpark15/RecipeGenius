import streamlit as st
from utils.generate_pdf import generate_pdf

class ChatInterface:
    def __init__(self, state_manager_, openai_service, image_service):
        self.state_manager = state_manager_
        self.openai_service = openai_service
        self.image_service = image_service
    
    def run(self):
        for msg in self.state_manager.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        self.state_manager.show_initial_message()        

        if st.session_state["initial_message_shown"]:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Ingredients"):
                    self.state_manager.set_button_clicked("ingredients")
            with col2:
                if st.button("Ideas"):
                    self.state_manager.set_button_clicked("ideas")
            
            # Add CSS to adjust button positioning
            st.markdown("""
                <style>
                    .stButton > button {
                        width: 100%;  /* Make buttons span the full width of their column */
                        padding: 15px; /* Adjust padding to make buttons more visually balanced */
                        font-size: 16px; /* Adjust font size */
                    }
                </style>
            """, unsafe_allow_html=True)
        
        if self.state_manager.button_clicked:
            self.handle_button_click()

        user_input = st.chat_input("Enter your message:")
        if user_input and user_input.strip():
            self.process_user_input(user_input)
        
    def handle_button_click(self):
        button_action = self.state_manager.button_clicked
        if button_action == "ingredients":
            message = "Great! List the ingredients you have, and I'll suggest a recipe."
        elif button_action == "ideas":
            message = "Awesome! Do you have any preferences? Vegetarian, spicy, quick meals?"
        
        self.state_manager.add_message("assistant", message)
        st.chat_message("assistant").write(message)
        self.state_manager.reset_button_clicked()

    def process_user_input(self, user_input):
        self.state_manager.add_message("user", user_input)
        st.chat_message("user").write(user_input)

        user_profile = {}

        user_ingredients = [ingredient.strip().lower() for ingredient in user_input.split(",")]

        dietary_preference = st.session_state["profile"].get("dietary_preference")
        if dietary_preference:
            user_profile["dietary_preference"] = dietary_preference
        
        allergies = st.session_state["profile"].get("allergies")
        if allergies:
            user_profile["allergies"] = allergies

        check_allergies = self.state_manager.check_allergies(user_ingredients)
        check_diet = self.state_manager.check_diet(user_ingredients)

        if check_allergies:
            # If an allergen is found, notify the user and do NOT proceed further
            warning_message = f"🚨 Sorry, but you included something you are allergic to: {check_allergies}. Would you like to provide different ingredients?"
            st.chat_message("assistant").write(warning_message)
            st.session_state.messages.append({"role": "assistant", "content": warning_message})
    
        elif dietary_preference == "Vegan" and check_diet:
            warning_message = f"🚨 The ingredient(s) {', '.join(check_diet)} are not suitable for a Vegan diet. Would you like to provide different ingredients?"
            st.chat_message("assistant").write(warning_message)
            st.session_state.messages.append({"role": "assistant", "content": warning_message})

        # Vegetarian warning
        elif dietary_preference == "Vegetarian" and check_diet:
            warning_message = f"🚨 The ingredient(s) {', '.join(check_diet)} are not suitable for a Vegetarian diet. Would you like to provide different ingredients?"
            st.chat_message("assistant").write(warning_message)
            st.session_state.messages.append({"role": "assistant", "content": warning_message})

        else:
            # Get response from OpenAI
            with st.spinner("Looking for the perfect dish...almost ready!"):
                response, is_recipe = self.openai_service.generate_recipe(self.state_manager.messages, user_profile)
            
            self.state_manager.add_message("assistant", response)
            st.chat_message("assistant").write(response)

            if is_recipe:
                self.generate_image(response)

                st.session_state["final_recipe"] = response
                st.session_state["final_recipe_message"] = user_input

                self.show_save_recipe_button()

            self.ask_follow_up()
    
    def generate_image(self, recipe_text):
        with st.spinner("Generating image of the plate..."):
            image = self.image_service.generate_image(recipe_text)
            if image:
                st.session_state["generated_image"] = image
                st.markdown("""
                    <style>
                        .stImage img {
                            display: block;
                            margin-left: auto;
                            margin-right: auto;
                            width: 500px;
                        }
                    </style>
                """, unsafe_allow_html=True)
                st.image(image, caption="Generated Image", use_container_width=False)
            else:
                st.error("Image generation failed. Please try again later.")
    
    def ask_follow_up(self):
        follow_up_message = "Would you like to try another recipe or need anything else?"
        self.state_manager.add_message("assistant", follow_up_message)
        st.chat_message("assistant").write(follow_up_message)

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, let's try again!"):
                    st.write("Button 1")

                    self.state_manager.reset_session()
                    st.experimental_rerun()

            with col2:
                if st.button("No, I'm done for now!"):
                    st.write("Button 2")
                    message = "Thanks for using RecipeGenius! Have a great day!"
                    self.state_manager.add_message("assistant", message)
                    st.chat_message("assistant").write(message)
                    self.state_manager.reset_session()

    def show_save_recipe_button(self):
        last_message = st.session_state["messages"][-1]
        if last_message["role"] == "assistant":
            recipe_text = last_message["content"]

            pdf_file = generate_pdf(recipe_text)
            
            st.download_button(
                label="Download Recipe as PDF",
                data=pdf_file,
                file_name="recipe.pdf",
                mime="application/pdf",
                icon=":material/download:",
            )
