# RecipeGenius

<div align="center">
  <h2 align="center">RecipeGenius 🧞</h1>
  <p align="center">
    Your Personal Recipe Curator!
  </p>
</div>

## About The Project

![recipegeniuspreview](https://github.com/user-attachments/assets/2bee70ae-be93-4aef-b9df-db289be7e39e)

Imagine having a world-class chef with unmatched creativity working with you personally to create the best dishes and drinks. Sounds like a great deal right? 

This becomes reality with RecipeGenius, your personal AI assistant for the kitchen. 
This wrapper application leverages generative AI to create a chatbot engineered to provide tailored meals and drinks recipe for each occasion.
Specify particular ingredients to use, or just bounce ideas to RecipeGenius -- date night, easy breakfast, low-calorie Mediterranean, whatever your heart desires!


This project is part of Grad 5900: Applied Generative AI at the University of Connecticut-Storrs.


## Getting Started

To get a local copy up and running follow these simple example steps.

### Installation

1. Get a free API Key at [https://openrouter.ai](https://openrouter.ai/)
2. Clone the repo
   ```sh
   git clone https://github.com/heraldpark15/RecipeGenius
   ```
3. Enter your API in `config.py`
   ```py
   API_KEY = 'ENTER YOUR API'
   ```
4. Run application through `main.py`
   ```sh
   streamlit run main.py
   ```
5. Enjoy!

## Usage

### Sidebar Features
![sidebar](https://github.com/user-attachments/assets/3bb99dea-22b8-466e-9614-8c3eb02c7acd)

_The sidebar allows users to specify dietary preferences and allergies. If you would like, please select one of the dietary preferences from the dropdown menu. Allergies can be inputted in the text input field. Multiple allergies can be inputted at once with each allergen separated with commas. Your profile can be continuously updated at any time, and this will instruct the LLM to consider your profile prior to recommending recipes._

### Recipe Download

_Once recipes are created, users have the option to download the output as a PDF file for future purposes._
## Tools Utilized

- HuggingFace Stable Diffusion 2
- DeepSeek R1
- Python
- Streamlit
- CSS

## Collaborators

[Adriana Iglesias Pedrejón](https://www.linkedin.com/in/adriana-iglesias-pedrej%C3%B3n-18b212225/) <br/>
[Herald Park](https://www.linkedin.com/in/heraldpark/)
