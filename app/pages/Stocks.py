# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp

# Global Variables
theme_plotly = None # None or streamlit
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Layout
st.set_page_config(page_title='Stock Analysis', page_icon=':bar_chart:', layout='wide')
st.title('💸 Stock Analysis')

# -- Choose stocks from stockslists
stocks_selected = st.sidebar.multiselect("Stock list", stocklist)
stocks = []
stocks.append("DATE")
for i in stocks_selected:
    stocks.append(search_dictio.get(i).upper())

# -- Choose the start and end dates
min_date = data[DATE_COLUMN].min()
max_date = data[DATE_COLUMN].max()
start_date = st.sidebar.date_input(
    "Start date:", min_value=min_date, max_value=max_date, value=min_date
)
end_date = st.sidebar.date_input(
    "End date:", min_value=min_date, max_value=max_date, value=max_date
)
st.write("Selected range:", start_date, "to", end_date)
    
returns = 
if len(stocks_selected) > 1:
        st.metric(
            "Total returns of stocks for the period",
            f"${returns.current_value.sum():.2f}",
            f"{returns.total_gain_loss_dollar.sum():.2f}",
        )
