import streamlit as st

class Sidebar:
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        st.sidebar.subheader("🎯 Personalize Your Experience")
        
        dietary_preference = st.sidebar.selectbox(
            "Dietary Preferences:", ["Select", "Vegetarian", "Vegan", "None"]
        )
        
        allergies = st.sidebar.text_area("Allergies (comma-separated):", placeholder="e.g., nuts, gluten")
        
        self.state_manager.update_user_profile(dietary_preference, allergies)

        st.sidebar.write("### Your Profile:")
        st.sidebar.write(f"**Dietary Preference:** {self.state_manager.profile['dietary_preference']}")
        st.sidebar.write(f"**Allergies:** {', '.join(self.state_manager.profile['allergies']) if self.state_manager.profile['allergies'] else 'None'}")