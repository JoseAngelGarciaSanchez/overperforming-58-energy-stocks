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


st.subheader("Presentation Twitter")
st.write(
    """    
    Twitter is a social media platform that allows users to post short messages, called tweets, which can contain text, images, and videos. These tweets can be viewed by other users, who can also interact with them by replying, re-tweeting, or liking them.
    From a web scraping point of view, Twitter can be accessed through its website, which is built using a combination of HTML, CSS, and JavaScript. To scrape data from Twitter, one would need to send HTTP requests to the Twitter server, which would return the HTML of the webpage. This HTML can then be parsed using a library such as Selenium to extract the desired data, such as tweets, 
    user information, and follower counts.
    It's important to note that scraping data from Twitter is against the company's terms of service, and it is not recommended to scrape the data without permission. Also, Twitter has some security mechanisms that prevent scraping like CAPTCHA, IP blocking and rate limiting
    """
)

st.subheader("Example of webscrapped dataset")
st.dataframe()

st.subheader("Methodology")
st.write(
    """    
    Improving the performance of 58 energy stocks. 
    To do this, we use webscrapping on tweets for the 58 stocks by classifying, then we classify in positif or negatif each of them thanks to a NLP model. 
    Then, in t+1 towards the tweet date, we buy or sell the stocks based on the analyzed tweets. If tweets on october 2021 are mostly positives, then we decide to buy the company stock. 
    This could be completed by news on bloomberg or other media such as bolsamania.
    """
)

st.subheader("Results")

st.subheader("About us")
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
