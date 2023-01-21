import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# from Home import load_data

# Global Variables
DATE_COLUMN = "DATE"
DATA_PATH = "./../data/stocks_data.xlsx"

# Layout
st.set_page_config(page_title="Home", page_icon=":bar_chart:", layout="wide")
st.title("Does Twitter have influence in stocks?")


st.markdown(
    """
 * Use the menu at left to select data and set plot parameters for analysis
"""
)
c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
stock_list = [
    "bp",
    "exxonmobil",
    "diamondbacks",
    "totalenergies",
    "upm",
    "chevron",
    "newmont",
]
for i, stock in enumerate(stock_list):
    logo_path = f"images/{stock}-logo.png"
    if i == 0:
        c1.image(Image.open(logo_path))
    elif i == 1:
        c2.image(Image.open(logo_path))
    elif i == 2:
        c3.image(Image.open(logo_path))
    elif i == 3:
        c4.image(Image.open(logo_path))
    elif i == 4:
        c5.image(Image.open(logo_path))
    elif i == 5:
        c6.image(Image.open(logo_path))
    elif i == 6:
        c7.image(Image.open(logo_path))

st.subheader('Methodology')
st.write(
    """    
    Improving the performance of 58 energy stocks. 
    To do this, we web scraping tweets for the 58 stocks by classifying each of them thanks to a NLP model that we have built. 
    Then, in t+1 we buy or sell the stocks based on the analyzed tweets. 
    This could be completed by news on bloomberg or other media such as bolsamania.
    """
)

st.subheader('Results')

st.subheader('About us')
# -- Aknowledgments
c1, c2 = st.columns(2)
with c1:
    st.info(
        "**Data Scientists Linkedin: [@JAGS](https://www.linkedin.com/in/jagarciasanchez) [@Sarra](https://www.linkedin.com/in/sarrabenyahia/)**",
        icon="💡",
    )
with c2:
    st.info(
        "**GitHub: [@JAGS](https://github.com/Pse1234) [@Sarra](https://github.com/sarrabenyahia)**",
        icon="💻",
    )
