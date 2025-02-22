import streamlit as st
from openai import OpenAI

# Sidebar for OpenAI API Key
with st.sidebar:
    openai_api_key = st.text_input("Enter Your API Key", key="chatbot_api_key", type="password")

# App title
st.title("RecipeGenius 🧞 - From Ingredients to Plate 🍽️")

content = '''
Hey! I'm a recipe bot for meals and drinks
'''

# Ensure API key is provided
if not openai_api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to continue.")
    st.stop()


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

# completion = client.chat.completions.create(
#   extra_headers={
#     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#   },
#   extra_body={},
#   model="deepseek/deepseek-r1:free",
#   messages=[
#     {
#       "role": "user",
#       "content": "What is your name?"
#     }
#   ]
# )
# print(completion.choices[0].message.content)

# Initialize session state for user profile
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {
        "goal": None,
        "experience": None,
        "workout_type": None
    }

# Sidebar user profile setup
st.sidebar.subheader("🎯 Personalize Your Experience")

goal = st.sidebar.selectbox("What's your fitness goal?", 
                            ["Select", "Weight Loss", "Muscle Gain", "Endurance", "General Fitness"])
experience = st.sidebar.selectbox("What's your experience level?", 
                                  ["Select", "Beginner", "Intermediate", "Advanced"])
workout_type = st.sidebar.selectbox("Preferred Workout Type:", 
                                    ["Select", "Strength Training", "Cardio", "Yoga", "Mixed"])

if goal != "Select":
    st.session_state["user_profile"]["goal"] = goal
if experience != "Select":
    st.session_state["user_profile"]["experience"] = experience
if workout_type != "Select":
    st.session_state["user_profile"]["workout_type"] = workout_type

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a recipe idea generator that helps create unique, interesting dishes and drinks."},
        {"role": "assistant", "content": "Hey friend! I'm here to help you plan your whole meal, from the ingredients to the drinks. Would you like to provide ingredients to use or an idea of what you want?"}
    ]
    st.session_state["button_clicked"] = None



# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Display buttons only after the first assistant message
if not st.session_state["button_clicked"]:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ingredients"):
            st.session_state["button_clicked"] = "ingredients"
    with col2:
        if st.button("Ideas"):
            st.session_state["button_clicked"] = "ideas"

# Handle button click responses
if st.session_state["button_clicked"] == "ingredients":
    msg = "Great! Please list the ingredients you have, and I'll suggest a recipe."
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    st.session_state["button_clicked"] = None  # Reset to allow further interaction

elif st.session_state["button_clicked"] == "ideas":
    msg = "Awesome! Do you have any preferences? For example, vegetarian, spicy, quick meals?"
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    st.session_state["button_clicked"] = None  # Reset to allow further interaction

# Chat input
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=st.session_state.messages
    )
    msg = response.choices[0].message.content

    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
