import streamlit as st



# Set page configuration
st.set_page_config(
    page_title="Contact",
    page_icon="🆒"
)

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# Page title and header
st.title("CNS:")

# Display address information
st.markdown(
    """
    <address>
        1140 W. Pender St., Suite 950 <br />
        Vancouver, BC, V6E 4G1 <br />
        <abbr title="Phone">P:</abbr>
        1.604.418.7872
    </address>
    <address>
        <strong>Support:</strong> <a href="mailto:Support@centralnervoussystems.com">Support@centralnervoussystems.com</a><br />
    </address>
    """, 
    unsafe_allow_html=True
)

# Sidebar message
#st.sidebar.success("Select a Dashboard from above.")
