import streamlit as st

class ChatInterface:
    def __init__(self, state_manager_, openai_service, image_service):
        self.state_manager = state_manager_
        self.openai_service = openai_service
        self.image_service = image_service
    
    def run(self):
        for msg in self.state_manager.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        if not self.state_manager.button_clicked:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Ingredients"):
                    self.state_manager.set_button_clicked("ingredients")
            with col2:
                if st.button("Ideas"):
                    self.state_manager.set_button_clicked("ideas")
        
        if self.state_manager.button_clicked:
            self.handle_button_click()

        self.state_manager.show_initial_message()        

        user_input = st.chat_input("Enter your message:")
        if user_input:
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

        # Get response from OpenAI
        with st.spinner("Generating recipe..."):
            response = self.openai_service.generate_recipe(self.state_manager.messages)
        
        self.state_manager.add_message("assistant", response)
        st.chat_message("assistant").write(response)

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
                if st.button("Yes, give me another recipe!"):
                    self.state_manager.reset_session()
                    st.experimental_rerun()

            with col2:
                if st.button("No, I'm done for now!"):
                    self.state_manager.reset_session()
                    st.write("Thanks for using RecipeGenius! Have a great day!")

    def show_save_recipe_button(self):
        save_button = st.button("Click here to save this recipe")
        if save_button:
            st.session_state["saved_recipe"] = st.session_state["final_recipe"]
            if "generated_image" in st.session_state:
                st.session_state["saved_recipe_image"] = st.session_state["generated_image"]
            
            st.success("Your recipe and image have been saved!")
            if "saved_recipe_iamge" in st.session_state:
                st.image(st.session_state["saved_recipe_image"], caption="Saved Recipe Image")
    
    def display_saved_recipe_and_image(self):
        if "saved_recipe" in st.session_state:
            st.subheader("Saved Recipe:")
            st.write(st.session_state["saved_recipe"])
        
        if "saved_recipe_image" in st.session_state:
            st.subheader("Recipe Image")
            st.image(st.session_state["saved_recipe_image"], caption="Saved Recipe Image")