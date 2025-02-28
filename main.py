import streamlit as st
from ui.sidebar import Sidebar
from ui.chat_interface import ChatInterface
from services.openai_service import OpenAIService
from services.image_service import ImageService
from utils.state_manager import StateManager

st.title("RecipeGenius 🧞 - From Ingredients to Plate 🍽️")

# Initialize state and services
state_manager = StateManager()
openai_service = OpenAIService()

# Sidebar setup
sidebar = Sidebar(state_manager)
sidebar.display()

# Chat interface
chat_interface = ChatInterface(state_manager, openai_service, ImageService)
chat_interface.run()
