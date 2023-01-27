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
    "STORA ENSO OYJ-R SHS",
    "INTERNATIONAL PAPER CO",
    "UPM-KYMMENE OYJ",
    "NEWMONT CORP",
    "EXXON MOBIL CORP",
    "VALERO ENERGY CORP",
    "NUCOR CORP",
    "BARRICK GOLD CORP",
    "FMC CORP",
    "FREEPORT-MCMORAN INC",
    "TOTALENERGIES SE",
    "CONOCOPHILLIPS",
    "ARCHER-DANIELS-MIDLAND CO",
    "POSCO HOLDINGS INC -SPON ADR",
    "BHP GROUP LTD-SPON ADR",
    "TECK RESOURCES LTD-CLS B",
    "RIO TINTO PLC-SPON ADR",
    "WILMAR INTERNATIONAL LTD",
    "MONDI PLC",
    "ANGLO AMERICAN PLC",
    "CENOVUS ENERGY INC",
    "ALTAGAS LTD",
    "WESTLAKE CORP",
    "GLENCORE PLC",
    "MOSAIC CO/THE",
    "MARATHON PETROLEUM CORP",
    "PHILLIPS 66",
    "WEYERHAEUSER CO",
    "ENERGY TRANSFER LP",
    "VIPER ENERGY PARTNERS LP",
    "SUNOCO LP",
    "WESTROCK CO",
    "PEMBINA PIPELINE CORP",
    "ALCOA CORP",
    "ARCELORMITTAL",
    "NUTRIEN CT LTD",
    "NUTRIEN US LTD",
    "DOW INC",
    "CORTEVA INC",
    "OCCIDENTAL PETROLEUM CORP",
    "ONEOK INC",
    "CHEVRON CORP",
    "PIONEER NATURAL RESOURCES CO",
    "TARGA RESOURCES CORP",
    "SCHLUMBERGER LTD",
    "BAKER HUGHES CO",
    "DEVON ENERGY CORP",
    "HESS CORP",
    "MARATHON OIL CORP",
    "WILLIAMS COS INC",
    "COTERRA ENERGY INC",
    "APA CORP",
    "EOG RESOURCES INC",
    "KINDER MORGAN INC",
    "EQT CORP",
    "HALLIBURTON CO",
    "DIAMONDBACK ENERGY INC",
    "S&P 500 ENERGY INDEX",
]

df_columns_list = [
    "BP/ LN Equity",
    "STERV FH Equity",
    "IP US Equity",
    "UPM FH Equity",
    "NEM US Equity",
    "XOM US Equity",
    "VLO US Equity",
    "NUE US Equity",
    "ABX CT Equity",
    "FMC US Equity",
    "FCX US Equity",
    "TTE FP Equity",
    "COP US Equity",
    "ADM US Equity",
    "PKX US Equity",
    "BHP US Equity",
    "TECK/B CT Equity",
    "RIO US Equity",
    "WIL SP Equity",
    "MNDI LN Equity",
    "AAL LN Equity",
    "CVE CT Equity",
    "ALA CT Equity",
    "WLK US Equity",
    "GLEN LN Equity",
    "MOS US Equity",
    "MPC US Equity",
    "PSX US Equity",
    "WY US Equity",
    "ET US Equity",
    "VNOM UW Equity",
    "SUN US Equity",
    "WRK US Equity",
    "PBA US Equity",
    "AA US Equity",
    "MTS SQ Equity",
    "NTR CT Equity",
    "NTR US Equity",
    "DOW US Equity",
    "CTVA US Equity",
    "OXY US Equity",
    "OKE US Equity",
    "CVX US Equity",
    "PXD US Equity",
    "TRGP US Equity",
    "SLB US Equity",
    "BKR US Equity",
    "DVN US Equity",
    "HES US Equity",
    "MRO US Equity",
    "WMB US Equity",
    "CTRA US Equity",
    "APA US Equity",
    "EOG US Equity",
    "KMI US Equity",
    "EQT US Equity",
    "HAL US Equity",
    "FANG US Equity",
    "S5ENRS Index",
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

st.write(options)
# Single chain Analysis
elif len(options) == 1:
    st.subheader('Overview')

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label='**Total Returns**', value=str(returns[options].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Transactions/Block**', value=str(df['Transactions/Block'].map('{:,.0f}'.format).values[0]))