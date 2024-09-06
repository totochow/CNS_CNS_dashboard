import streamlit as st
import clr  # Import the pythonnet library
import os
from datetime import datetime
import requests

# Add reference to your C# DLL
dll_path = r'C:\Program Files (x86)\MISys\MISys SBM\MISys SBM 6.4 Client\MISys.API.dll'
clr.AddReference(dll_path)

# Import the namespace and class from the C# DLL
from MISys.API import MIAPI  # type: ignore

# Function to get user's IP address
def get_user_ip():
    try:
        ip = requests.get('https://api.ipify.org').text
    except requests.RequestException:
        ip = 'IP not available'
    return ip

# Initialize API
def init_api(userId, password):
    login_value = False
    # Configuration settings
    config = {
        'CNS_ServerURL': st.secrets.cns.serverurl,
        'CNS_CompanyName': st.secrets.cns.cnscompanyname,
        'CNS_UserName': userId.upper(),
        'CNS_Password': password
    }
    try:
        # Initialize the MIAPI class
        api = MIAPI(
            config['CNS_ServerURL'],
            config['CNS_CompanyName'],
            config['CNS_UserName'],
            config['CNS_Password'], True
        )

        log_file_path = f"C:\\CNS\\LOG\\{datetime.now().strftime('%Y%m%d')}ServiceLOGs.txt"
        
        with open(log_file_path, 'a') as log_file:
            ip_address = get_user_ip()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if api.Logon() == 1:  # Adjust based on actual method and return value
                log_file.write(f"Timestamp: {timestamp}, SUCCESS, Logged on as {userId.upper()}\n")
                api.Logoff()
                login_value = True
                    
            else:
                log_file.write(f"Timestamp: {timestamp}, FAILED, Log on Attempted as {userId.upper()}\n")
                
    except Exception as e:
        log_file_path = f"C:\\CNS\\LOG\\{datetime.now().strftime('%Y%m%d')}ServiceLOGs.txt"
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"Timestamp: {timestamp}, EXCEPTION OCCURED,  Log on Attempted as {userId.upper()}, Error: {str(e)}\n")
        login_value = False
    
    return login_value

st.set_page_config(
    page_title="Login",
    page_icon="🔒",
    layout="centered"
)

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# Check if the user is authenticated
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    st.title("CNS MISys Dashboard Project")
    st.markdown("_v.0.0.001_")
    
else:
    st.title("Login Page")
    st.markdown("_Please log in to access the dashboard._")
    # Display the login form
    userId = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if init_api(userId, password):
            st.session_state.authenticated = True
            st.session_state.userId = userId
            st.rerun()
        else:
            st.error("Login failed. Please check your credentials.")
            st.stop()
