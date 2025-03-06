import streamlit as st
from openai import OpenAI
from imageGeneration import generate_image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from io import BytesIO

# Sidebar for OpenAI API Key
with st.sidebar:
    openai_api_key = st.text_input("Enter Your API Key", key="chatbot_api_key", type="password")

# App title
st.title("RecipeGenius 🧞 - From Ingredients to Plate 🍽️")

# Ensure API key is provided
if not openai_api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to continue.")
    st.stop()

openai_api_key = ""  # Replace with your actual key

os.environ["OPENAI_API_KEY"] = openai_api_key

client = OpenAI()

def generate_pdf(recipe_text):
    """Creates a PDF file in memory with the given recipe text."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    
    y_position = 750  # Start position for text
    for line in recipe_text.split("\n"):
        pdf.drawString(50, y_position, line)
        y_position -= 20  # Move down for the next line

    pdf.save()
    buffer.seek(0)
    return buffer

# Initialize session state for user profile and other variables
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {
        "dietary_preference": None, 
        "allergies": []
    }

# Ensure 'button_clicked' and 'messages' are initialized
if "button_clicked" not in st.session_state:
    st.session_state["button_clicked"] = None  # Initialize button state to None

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a recipe idea generator that helps create unique, interesting dishes and drinks."}
    ]


# Sidebar user profile setup
st.sidebar.subheader("🎯 Personalize Your Experience")

# Dietary preferences options
dietary_preference = st.sidebar.selectbox("Do you have any dietary preferences?", 
                                          ["Select", "Vegetarian", "Vegan", "None"])

# Input for allergies
allergies = st.sidebar.text_area("List your allergies (comma separated, e.g., nuts, gluten)", 
                                 placeholder="e.g., nuts, gluten")

if dietary_preference != "Select":
    st.session_state["user_profile"]["dietary_preference"] = dietary_preference
if allergies:
    st.session_state["user_profile"]["allergies"] = [allergy.strip() for allergy in allergies.split(",")]

# Display the user's saved profile data
st.sidebar.write("### Your Profile:")
st.sidebar.write(f"**Dietary Preference:** {st.session_state['user_profile']['dietary_preference']}")
st.sidebar.write("**Allergies:**")
if st.session_state['user_profile']['allergies']:
    st.sidebar.write(f"- {', '.join(st.session_state['user_profile']['allergies'])}")
else:
    st.sidebar.write("None")

# Display initial message only once
if "initial_message_shown" not in st.session_state:
    st.session_state["initial_message_shown"] = False

if not st.session_state["initial_message_shown"]:
    st.session_state["initial_message_shown"] = True
    initial_message = "Hey friend! I'm here to help you plan your whole meal, from the ingredients to the drinks. Would you like to provide ingredients to use or an idea of what you want?"
    st.session_state.messages.append({"role": "assistant", "content": initial_message})
    st.chat_message("assistant").write(initial_message)

# Display the buttons only once after the initial message
if st.session_state["initial_message_shown"]:
    col1, col2 = st.columns([1, 1])  # Equal width columns for the buttons

    with col1:
        if st.button("Ingredients"):
            st.session_state["button_clicked"] = "ingredients"
            st.session_state["initial_message_shown"] = False  # Prevent button from showing again
    
    with col2:
        if st.button("Ideas"):
            st.session_state["button_clicked"] = "ideas"
            st.session_state["initial_message_shown"] = False  # Prevent button from showing again

    # Add custom CSS to adjust button positioning
    st.markdown("""
        <style>
            .stButton > button {
                width: 100%;  /* Make buttons span the full width of their column */
                padding: 15px; /* Adjust padding to make buttons more visually balanced */
                font-size: 16px; /* Adjust font size */
            }
        </style>
    """, unsafe_allow_html=True)

# Handle button click responses
if st.session_state["button_clicked"] == "ingredients":
    msg = "Great! Please list the ingredients you have, and I'll suggest a recipe considering your dietary preferences and allergies."
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    st.session_state["button_clicked"] = None  # Reset to allow further interaction

elif st.session_state["button_clicked"] == "ideas":
    msg = "Awesome! Do you have any preferences? For example, vegetarian, spicy, quick meals?"
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    st.session_state["button_clicked"] = None  # Reset to allow further interaction

# Chat input for recipe generation
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Create a custom prompt considering dietary preferences and allergies
    dietary_preference = st.session_state["user_profile"]["dietary_preference"]
    allergies = st.session_state["user_profile"]["allergies"]
    non_vegetarian_ingredients = ['chicken', 'beef', 'pork', 'lamb', 'fish', 'shrimp', 'bacon', 'turkey', 'duck']
    non_vegan_ingredients = ['chicken', 'beef', 'pork', 'lamb', 'fish', 'shrimp', 'bacon', 'turkey', 'duck', 'milk', 'cheese', 'butter', 'eggs', 'honey']
    
    user_ingredients = [ingredient.strip().lower() for ingredient in prompt.split(",")]
    
    allergens_found = [allergen for allergen in allergies if allergen.lower() in user_ingredients]
    
    non_veg_found = [ingredient for ingredient in user_ingredients if ingredient in non_vegetarian_ingredients]
    non_vegan_found = [ingredient for ingredient in user_ingredients if ingredient in non_vegan_ingredients]


    if allergens_found:
        # If an allergen is found, notify the user and do NOT proceed further
        warning_message = f"🚨 Sorry, but you included something you are allergic to: {', '.join(allergens_found)}. Would you like to provide different ingredients?"
        st.chat_message("assistant").write(warning_message)
        st.session_state.messages.append({"role": "assistant", "content": warning_message})
    
    elif dietary_preference == "Vegan" and non_vegan_found:
        warning_message = f"🚨 The ingredient(s) {', '.join(non_vegan_found)} are not suitable for a Vegan diet. Would you like to provide different ingredients?"
        st.chat_message("assistant").write(warning_message)
        st.session_state.messages.append({"role": "assistant", "content": warning_message})

    # Vegetarian warning
    elif dietary_preference == "Vegetarian" and non_veg_found:
        warning_message = f"🚨 The ingredient(s) {', '.join(non_veg_found)} are not suitable for a Vegetarian diet. Would you like to provide different ingredients?"
        st.chat_message("assistant").write(warning_message)
        st.session_state.messages.append({"role": "assistant", "content": warning_message})

    else:

        system_message = '''
                    "You are a recipe generator. Provide recipes in this format:\n"
                    "1. Title of the Dish\n2. List of ingredients\n3. Steps to prepare\n"
                    "4. Suggested Drink Pairing (with ingredients)"
                    "Do not include any reasoning, inner thoughts, or additional explanations. Only provide the recipe in the specified format. Avoid repeating recipes you've suggested earlier."
                    "If the user asks about content that is not related to recipe generation, please reply with 'Sorry, I am not equipped to answer questions unrelated to recipe generation'"
                '''
        if dietary_preference:
                system_message += f"\nPlease make sure the recipe is suitable for a {dietary_preference} diet."
        if allergies:
                system_message += f"\nAvoid including the following allergens in the recipe: {allergies}."
        

        with st.spinner("Looking for the perfect dish... almost ready!"):
            # Make API request to OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system_message}] + 
                        [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages if msg["role"] in ["user", "assistant"]]
            )

        msg = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)


        # Generate image of the plate based on the dish description
        with st.spinner("Generating image of the plate..."):
            image = generate_image(msg)  # Generate image from the recipe text
            if image:
                # Apply custom CSS to center the image
                st.markdown("""
                    <style>
                        .stImage img {
                            display: block;
                            margin-left: auto;
                            margin-right: auto;
                            width: 500px;  /* Adjust image width */
                        }
                    </style>
                """, unsafe_allow_html=True)
                
                st.image(image, caption="Generated Image", use_container_width=False)
            else:
                st.error("Image generation failed. Please try again later.")

        if "messages" in st.session_state and st.session_state["messages"]:
            last_message = st.session_state["messages"][-1]
            if last_message["role"] == "assistant":
                recipe_text = last_message["content"]

                # Create PDF from recipe text
                pdf_file = generate_pdf(recipe_text)

                # Add a download button
                st.download_button(
                    label="📥 Download Recipe as PDF",
                    data=pdf_file,
                    file_name="recipe.pdf",
                    mime="application/pdf"
                )

        follow_up_message = "Would you like to try another recipe or need anything else?"
        st.session_state.messages.append({"role": "assistant", "content": follow_up_message})
        st.chat_message("assistant").write(follow_up_message)

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, give me another recipe!"):
                    # Logic for generating another recipe or resetting
                    st.session_state["button_clicked"] = None  # Reset button state
                    st.session_state["messages"].clear()  # Clear previous messages to start fresh
                    st.experimental_rerun()  # Re-run the app to restart the process

            with col2:
                if st.button("No, I'm done for now!"):
                    st.session_state["button_clicked"] = None  # Reset state if needed
                    st.session_state["messages"].clear() 
                    st.session_state["initial_message_shown"] = False 
                    st.write("Thanks for using RecipeGenius! Have a great day!")  # Show the thank you message

