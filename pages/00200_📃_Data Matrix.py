import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px
from PIL import Image
from pylibdmtx import pylibdmtx

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# Ensure that this is placed after the authentication check
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.write("Please log in to access this page.")
    st.stop()  # Stop further execution of the script if not authenticated

def generate_datamatrix(data):
    # Generate the Data Matrix barcode
    encoded = pylibdmtx.encode(data.encode('utf8'))
    
    # Convert the result to an image
    image = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    
    # Return the image object
    return image

# Add an input field with a default value for the user to enter the text to encode
user_input = st.text_input("Enter text to generate Data Matrix barcode:", value="Hello World")

# Generate the Data Matrix barcode image based on user input
datamatrix_image = generate_datamatrix(user_input)

# Display the Data Matrix barcode image in the Streamlit app
st.image(datamatrix_image, caption="Generated Data Matrix Barcode")

