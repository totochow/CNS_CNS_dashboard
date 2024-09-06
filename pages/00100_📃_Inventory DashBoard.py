import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px
from PIL import Image



# Ensure that this is placed after the authentication check
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.write("Please log in to access this page.")
    st.stop()  # Stop further execution of the script if not authenticated

# Define your connection string
conn_str = (
    "Driver={SQL Server};"
    f"Server={st.secrets.cns.sqlserver};" 
    f"Database={st.secrets.cns.cnscompanyname};"
    f"Uid={st.secrets.cns.sqlusername};"
    f"Pwd={st.secrets.cns.sqlpassword};"
)

def load_company():
    conn = pyodbc.connect(conn_str)
    query = f"""
    SELECT coName 
    FROM [{st.secrets.cns.cnscompanyname}].[dbo].[MIOPTN]
    """
    coName=pd.read_sql(query, conn)
    conn.close()
    return coName

# Load the company name
MIOPTN_df = load_company()

# Extract the company name (assuming there's only one row in the result)
coName = MIOPTN_df.iloc[0]['coName'] if not MIOPTN_df.empty else "coName"

# Set the page config after fetching the company name
st.set_page_config(
    page_title=f"Inventory Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# print(conn_str)

# @st.cache_data
def load_data():
    # Create a connection
    conn = pyodbc.connect(conn_str)
    # Define the query
    query = """
    SELECT *
    FROM [MITESTCO].[dbo].[CNS_view_InvObsCostCalculation]
    """
    # Execute the query and load into a DataFrame
    data = pd.read_sql(query, conn)
    # Close the connection
    conn.close()
    return data

### --- LOAD DATAFRAME
df = load_data()

#with st.expander("Data Preview"):  
#    st.write(df)
st.title(f"{coName}: Inventory Dashboard")
# Arrange selectors in three columns at the top of the page
col1, col2 = st.columns(2)

with col1:
    item_types = df['ItemType'].unique().tolist()
    item_types_selection = st.multiselect('Item Type:', item_types, default=item_types)

with col2:
    expiry_status = df['ExpiryStatus'].unique().tolist()
    expiry_status_selection = st.multiselect('Expiry Status:', expiry_status, default=expiry_status)


# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['ItemType'].isin(item_types_selection) & df['ExpiryStatus'].isin(expiry_status_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# Group by 'ExpiryStatus' and aggregate both the count of 'itemId' and the sum of 'ExtendedCost'
df_grouped = df[mask].groupby(by=['ExpiryStatus']).agg(
    {'itemId': 'count', 'ExtendedCost': 'sum'})
# Rename columns
df_grouped = df_grouped.rename(columns={'itemId': '# of SKU', 'ExtendedCost': 'Total Extended Cost'})

# Reset the index to flatten the DataFrame
df_grouped = df_grouped.reset_index()


with st.expander("Data Preview"):
    st.dataframe(df_grouped, column_config={"Total Extended Cost":st.column_config.NumberColumn(format="$ %.2f")})

# Arrange bar charts in two columns
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # --- PLOT BAR CHART FOR '# of SKU'
    bar_chart_sku = px.bar(df_grouped,
                           x='ExpiryStatus',
                           y='# of SKU',
                           text='# of SKU',
                           color_discrete_sequence=['#F63366']*len(df_grouped),
                           template='plotly_white',
                           title= "# of Expiring SKUs")
    # Center the title at the top
    bar_chart_sku.update_layout(
        title={
            'text': "# of Expiring SKUs",
            'y': 0.9,  # Adjust the vertical position
            'x': 0.5,  # Center the title horizontally
            'xanchor': 'center',
            'yanchor': 'top'
        })
    
    # Show the chart in Streamlit
    st.plotly_chart(bar_chart_sku)

with chart_col2:
    # --- PLOT BAR CHART FOR 'Total Extended Cost'
    bar_chart_cost = px.bar(df_grouped,
                            x='ExpiryStatus',
                            y='Total Extended Cost',
                            text='Total Extended Cost',
                            color_discrete_sequence=['#636EFA']*len(df_grouped), 
                            template='plotly_white',
                            title= "Value of Expiring SKUs")

    # Adjust text formatting for currency display
    bar_chart_cost.update_traces(
        texttemplate='%{text:$,.2f}',  # Format as currency with $ and comma separators
        textposition='outside'
    )

    # Center the title at the top
    bar_chart_cost.update_layout(
        title={
            'text': "Value of Expiring SKUs",
            'y': 0.9,  # Adjust the vertical position
            'x': 0.5,  # Center the title horizontally
            'xanchor': 'center',
            'yanchor': 'top'
        }
)

    # Show the chart in Streamlit
    st.plotly_chart(bar_chart_cost)
