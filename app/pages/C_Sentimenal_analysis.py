import streamlit as st
import pandas as pd

# Global Variables
DATE_COLUMN = "DATE"
DATA_PATH = "./../model/model_df/model.csv"

# Layout
st.set_page_config(
    page_title="Sentimental analysis", page_icon=":bar_chart:", layout="wide"
)

st.title("Sentimental analysis on tweets: 📈 or 📉")
st.header("Finance define bullish 📈 and bearish 📉 as two tendencies on stocks")
st.subheader("If bullish is predicted in t, they recommend to buy on t+1. For us, t gonna be monthly.")

data = pd.read_csv(DATA_PATH)
st.dataframe(data)