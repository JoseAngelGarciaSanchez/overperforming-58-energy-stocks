# Libraries
import streamlit as st
import pandas as pd

# Global Variables
DATE_COLUMN = "DATE"
DATA_PATH = "./../data/stocks_data.xlsx"

# Layout
st.set_page_config(
    page_title="Tweets impact on stocks", page_icon=":bar_chart:", layout="wide"
)
st.title("Tweets impact on stocks 📈📉")

# Style
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache
def load_data():
    data = pd.read_excel(DATA_PATH, sheet_name="Returns", header=[5, 6]).T.iloc[2:, :]
    data = data.rename(columns=data.iloc[0])
    data = data.iloc[2:]
    upercase = lambda x: str(x).upper()
    data.rename(upercase, axis="columns", inplace=True)
    data.reset_index(inplace=True)
    data.rename(columns={"level_0": "DATE1", "level_1": "DATE"}, inplace=True)
    data.drop(columns="DATE1", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]).dt.date
    return data

returns = load_data()    

stocklist = [
    "BP PLC",
    "FMC CORP",
    "WEYERHAEUSER CO",
]

df_columns_list = [
    "BP/ LN Equity",
    "FMC US Equity",
    "WY US Equity",
]

search_dictio = {}
for i, k in enumerate(df_columns_list):
    search_dictio[stocklist[i]] = k


# Filter the blockchains
options = st.multiselect(
    '**Select your desired blockchains:**',
    options=stocklist,
    default=None,
    key='macro_options'
)


if len(options) == 0:
    st.warning('Please select at least one stock to see the metrics.')

elif len(options) == 1:
    st.subheader('Overview')

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label='**Total Returns**', value=str(returns[options].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Transactions/Block**', value=str(df['Transactions/Block'].map('{:,.0f}'.format).values[0]))

else:
    1