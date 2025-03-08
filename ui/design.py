import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
        @keyframes gradientAnimation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .stApp {
            background: linear-gradient(135deg, #ff758c, #ff7eb3, #a1c4fd, #c2e9fb);
            background-size: 300% 300%;
            animation: gradientAnimation 10s ease infinite;
            color: #333;
            font-family: Arial, sans-serif;
        }

        /* Floating Button Effect */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-5px); }
            100% { transform: translateY(0px); }
        }

        /* Styling Streamlit buttons */
        .stButton>button {
            background: linear-gradient(90deg, #ff758c, #ff7eb3);
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            animation: float 5s ease-in-out infinite;
        }

        /* Hover Effect for Buttons */
        .stButton>button:hover {
            background: linear-gradient(90deg, #a1c4fd, #c2e9fb);
            transform: scale(1.05);
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
        }

        /* Sidebar Styling */
        .stSidebar {
            color: white !important;
        }
        
        .stSidebar .stButton>button {
            background: linear-gradient(90deg, #6a11cb, #2575fc);
            animation: none; /* No floating in sidebar */
        }

        .stSidebar .stButton>button:hover {
            background: linear-gradient(90deg, #ff758c, #ff7eb3);
            transform: scale(1.05);
        }

        /* Slide-in Text Animation */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .slide-text {
            animation: slideIn 3s ease-out;
        }

        .stSidebar label {
            padding-left: 10px; /* Add left padding to sidebar labels */
        }

        /* Sidebar Profile Styling */
        .profile-text {
            color: #fff;
            font-size: 14px;
        }

        .stSidebar .profile-text {
            color: #e8e8e8; /* Lighter color for the sidebar text */
        }

        /* Recipe Text Styling */
        .saved-recipes {
            color: #fff;
            font-size: 14px;
            padding-top: 10px;
            padding-bottom: 10px;
        }
        
        /* Image Styling */
        .stImage img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 90%;
            border-radius: 8px;
        }

        .stSelectbox:hover {
            border-color: #ff7eb3;
        }

        .stDownloadButton > button {
            background: linear-gradient(90deg, #ff758c, #ff7eb3) !important;
            color: white !important;
            border: none !important;
            padding: 10px 20px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            cursor: pointer !important;
            transition: all 0.3s ease-in-out !important;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2) !important;
            animation: float 5s ease-in-out infinite !important;
        }

        /* Hover Effect */
        .stDownloadButton > button:hover {
            background: linear-gradient(90deg, #a1c4fd, #c2e9fb) !important;
            transform: scale(1.05) !important;
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3) !important;
        }

        /* Simple Text Input Styling */
        div[data-testid="stChatInput"] textarea {
            background-color: white !important;  /* Make the background white */
            border: none !important;             /* Remove the border */
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.2) !important;
            color: #333 !important;              /* Set the text color */
            padding: 10px !important;            /* Add some padding for a clean look */
            font-size: 16px !important;          /* Set the font size */
            font-family: Arial, sans-serif !important;  /* Set a clean font */
        }

        /* Remove the dark background when focused */
        div[data-testid="stChatInput"] textarea:focus {
            outline: none !important;            /* Remove the focus outline */
            border: none !important;             /* Ensure no border is added on focus */
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2) !important;
        }

        /* Ensure the placeholder text is visible and not affected */
        div[data-testid="stChatInput"] textarea::placeholder {
            color: #777 !important;             /* Set placeholder text color */
            font-style: italic !important;       /* Optionally, make it italic */
        }

        /* Remove the surrounding dark block */
        div.st-emotion-cache-hzygls {
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
        }

        /* Remove any background or borders from the header */
        header.stAppHeader {
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
            padding: 0 !important;  /* Remove any default padding */
        }

        header.stAppHeader h1, header.stAppHeader h2 {
            color: #fff !important;  /* Change header text color */
            font-family: Arial, sans-serif !important;  /* Customize font */
            font-weight: bold !important;  /* Make header text bold */
        }

        header.stAppHeader .stHeader .stButton {
            background: linear-gradient(90deg, #ff758c, #ff7eb3) !important;  /* Button gradient */
            color: white !important;
            border: none !important;
            padding: 10px 20px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            cursor: pointer !important;
            transition: all 0.3s ease-in-out !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )