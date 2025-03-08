import streamlit as st
from ui.sidebar import Sidebar
from ui.chat_interface import ChatInterface
from services.openai_service import OpenAIService
from services.image_service import ImageService
from utils.state_manager import StateManager
from ui.design import apply_styles

apply_styles()

#st.title("RecipeGenius 🧞 - From Ingredients to Plate 🍽️")
st.markdown('<h1 class="slide-text">RecipeGenius 🧞 - From Ingredients to Plate 🍽️</h1>', unsafe_allow_html=True)

# Initialize state and services
state_manager = StateManager()
openai_service = OpenAIService()

# Run sidebar
sidebar = Sidebar(state_manager)
sidebar.display()

# Chat interface
chat_interface = ChatInterface(state_manager, openai_service, ImageService)
chat_interface.run()
