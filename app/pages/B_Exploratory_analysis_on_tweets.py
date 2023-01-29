# Libraries
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import seaborn as sns

# Global Variables
DATE_COLUMN = "DATE"
DATA_PATH = "./../data/stocks_data.xlsx"
TWEETS_PATH = [
    "./../data_cleaned/webscraped_FMC_CORP.csv/part-00000-9fe4bf5d-f913-4d0c-a98a-8f1d088639ee-c000.csv",
    "./../data_cleaned/webscraped_WEYERHAEUSER_CO.csv/part-00000-17a4305d-9672-4ddf-87fc-d180dcf01612-c000.csv",
    "./../data_cleaned/webscraped_BP_PLC.csv/part-00000-8a74ec7d-2015-42d8-8960-ce8e11e5a3a2-c000.csv",
]

# Layout
st.set_page_config(
    page_title="Tweets analysis for stocks", page_icon=":bar_chart:", layout="wide"
)
st.title("Tweets analysis for stocks 📈📉")

# Style
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@st.cache
def load_data():
    returns = pd.read_excel(DATA_PATH, sheet_name="Returns", header=[5, 6]).T.iloc[
        2:, :
    ]
    returns = returns.rename(columns=returns.iloc[0])
    returns = returns.iloc[2:]
    upercase = lambda x: str(x).upper()
    returns.rename(upercase, axis="columns", inplace=True)
    returns.reset_index(inplace=True)
    returns.rename(columns={"level_0": "DATE1", "level_1": "DATE"}, inplace=True)
    returns.drop(columns="DATE1", inplace=True)
    returns[DATE_COLUMN] = pd.to_datetime(returns[DATE_COLUMN]).dt.date
    # we add fmc webscrapped data
    fmc_tweets = pd.read_csv(TWEETS_PATH[0])
    fmc_tweets["company"] = "FMC CORP"
    # we add wy webscrapped data
    wy_tweets = pd.read_csv(TWEETS_PATH[1])
    wy_tweets["company"] = "WEYERHAEUSER CO"
    # we add bp webscrapped data
    bp_tweets = pd.read_csv(TWEETS_PATH[2])
    bp_tweets["company"] = "BP PLC"
    tweets = pd.concat([fmc_tweets, wy_tweets, bp_tweets])
    tweets["PostDate"] = pd.to_datetime(tweets["PostDate"]).dt.date
    # we add a column with the length of each tweet
    tweets["tweet_length"] = tweets["TweetText"].apply(lambda x: len(x.split()))
    return returns, tweets


returns, tweets = load_data()

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


# Filter the stocks
options = st.multiselect(
    "**Select your desired blockchains:**",
    options=stocklist,
    default=None,
    key="macro_options",
)

min_date = tweets["PostDate"].min()
max_date = tweets["PostDate"].max()

# filter start date
start_date = st.date_input(
    "**Select a start date:**",
    min_value=min_date,
    max_value=max_date,
    value=min_date,
    key="start_date",
)
# filter end date
end_date = st.date_input(
    "**Select an end date:**",
    min_value=min_date,
    max_value=max_date,
    value=max_date,
    key="end_date",
)

condition1 = start_date <= tweets["PostDate"]
condition2 = tweets["PostDate"] <= end_date
mask = condition1 & condition2
filtered_tweets = tweets.loc[mask, :]

# Initialiser la variable des mots vides
stop_words = set(stopwords.words("english"))

if len(options) == 0:
    st.warning("Please select at least one stock to see the metrics.")

elif len(options) == 1:
    mask = filtered_tweets["company"] == options[0]
    filtered_tweets = filtered_tweets.loc[mask, :]
    st.subheader(f"Analytics for {options[0]} from {start_date} to {end_date}")
    st.metric(
        label=f"Number of tweets for {options[0]}:", value=str(filtered_tweets.shape[0])
    )
    #     st.metric(label='**Total Returns**', value=str(returns[options].map('{:,.0f}'.format).values[0]))
    #     st.metric(label='**Average Transactions/Block**', value=str(returns[options].map('{:,.0f}'.format).values[0]))

    # we select all the tweets from 2017 to 2022
    tweet_list = filtered_tweets["TweetText"].tolist()
    # join all tweets into a single string
    tweet_string = " ".join(tweet_list)

    # # we have decided to remove the name of the company because is our keyword
    # tweet_string = tweet_string.replace("weyerhaeuser", "").replace("co", "")

    # create the word cloud
    wordcloud = WordCloud(stopwords=stop_words).generate(tweet_string)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title(f"Wordcloud for {options[0]} from {start_date} to {end_date}")
    plt.axis("off")
    plt.show()

    def wordcloud_stock():
        st.pyplot(plt)

    wordcloud_stock()

    # frequency plot
    def frequency_tweets_length_stock():
        sns.set_style("darkgrid")
        sns.displot(filtered_tweets["tweet_length"], bins=20)
        plt.title(f"Tweet frequency length for {options[0]}")
        plt.xlabel("Tweet Length")
        plt.ylabel("Number of Tweets")
        plt.show()
        st.pyplot(plt)

    frequency_tweets_length_stock()

elif len(options) == 2:
    st.subheader(f'Analytics for {", ".join(options)} from {start_date} to {end_date}')
    c1, c2 = st.columns(2)

    with c1:
        mask_1 = filtered_tweets["company"] == options[0]
        filtered_tweets_1 = filtered_tweets.loc[mask_1, :]
        st.metric(
            label=f"Number of tweets for {options[0]}:",
            value=str(filtered_tweets_1.shape[0]),
        )

        # we select all the tweets from 2017 to 2022
        tweet_list = filtered_tweets_1["TweetText"].tolist()
        # join all tweets into a single string
        tweet_string = " ".join(tweet_list)

        # frequency plot
        def frequency_tweets_length_stock():
            sns.set_style("darkgrid")
            sns.displot(filtered_tweets_1["tweet_length"], bins=20)
            plt.title(f"Tweet frequency length for {options[0]}")
            plt.xlabel("Tweet Length")
            plt.ylabel("Number of Tweets")
            plt.show()
            st.pyplot(plt)

        frequency_tweets_length_stock()

        # create the word cloud
        wordcloud = WordCloud(stopwords=stop_words).generate(tweet_string)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.title(f"Wordcloud for {options[0]} from {start_date} to {end_date}")
        plt.axis("off")
        plt.show()

        def wordcloud_stock():
            st.pyplot(plt)

        wordcloud_stock()

    with c2:
        mask_2 = filtered_tweets["company"] == options[1]
        filtered_tweets_2 = filtered_tweets.loc[mask_2, :]
        st.metric(
            label=f"Number of tweets for {options[1]}:",
            value=str(filtered_tweets_2.shape[0]),
        )

        # we select all the tweets from 2017 to 2022
        tweet_list = filtered_tweets_2["TweetText"].tolist()
        # join all tweets into a single string
        tweet_string = " ".join(tweet_list)

        # frequency plot
        def frequency_tweets_length_stock():
            sns.set_style("darkgrid")
            sns.displot(filtered_tweets_2["tweet_length"], bins=20)
            plt.title(f"Tweet frequency length for {options[1]}")
            plt.xlabel("Tweet Length")
            plt.ylabel("Number of Tweets")
            plt.show()
            st.pyplot(plt)

        frequency_tweets_length_stock()

        # create the word cloud
        wordcloud = WordCloud(stopwords=stop_words).generate(tweet_string)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.title(f"Wordcloud for {options[0]} from {start_date} to {end_date}")
        plt.axis("off")
        plt.show()

        def wordcloud_stock():
            st.pyplot(plt)

        wordcloud_stock()

elif len(options) == 3:
    st.subheader(f'Analytics for {", ".join(options)} from {start_date} to {end_date}')
    c1, c2, c3 = st.columns(3)

    with c1:
        mask_1 = filtered_tweets["company"] == options[0]
        filtered_tweets_1 = filtered_tweets.loc[mask_1, :]
        st.metric(
            label=f"Number of tweets for {options[0]}:",
            value=str(filtered_tweets_1.shape[0]),
        )

        # we select all the tweets from 2017 to 2022
        tweet_list = filtered_tweets_1["TweetText"].tolist()
        # join all tweets into a single string
        tweet_string = " ".join(tweet_list)

        # frequency plot
        def frequency_tweets_length_stock():
            sns.set_style("darkgrid")
            sns.displot(filtered_tweets_1["tweet_length"], bins=20)
            plt.title(f"Tweet frequency length for {options[0]}")
            plt.xlabel("Tweet Length")
            plt.ylabel("Number of Tweets")
            plt.show()
            st.pyplot(plt)

        frequency_tweets_length_stock()

        # create the word cloud
        wordcloud = WordCloud(stopwords=stop_words).generate(tweet_string)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.title(f"Wordcloud for {options[0]} from {start_date} to {end_date}")
        plt.axis("off")
        plt.show()

        def wordcloud_stock():
            st.pyplot(plt)

        wordcloud_stock()

    with c2:
        mask_2 = filtered_tweets["company"] == options[1]
        filtered_tweets_2 = filtered_tweets.loc[mask_2, :]
        st.metric(
            label=f"Number of tweets for {options[1]}:",
            value=str(filtered_tweets_2.shape[0]),
        )

        # we select all the tweets from 2017 to 2022
        tweet_list = filtered_tweets_2["TweetText"].tolist()
        # join all tweets into a single string
        tweet_string = " ".join(tweet_list)

        # frequency plot
        def frequency_tweets_length_stock():
            sns.set_style("darkgrid")
            sns.displot(filtered_tweets_2["tweet_length"], bins=20)
            plt.title(f"Tweet frequency length for {options[1]}")
            plt.xlabel("Tweet Length")
            plt.ylabel("Number of Tweets")
            plt.show()
            st.pyplot(plt)

        frequency_tweets_length_stock()

        # create the word cloud
        wordcloud = WordCloud(stopwords=stop_words).generate(tweet_string)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.title(f"Wordcloud for {options[1]} from {start_date} to {end_date}")
        plt.axis("off")
        plt.show()

        def wordcloud_stock():
            st.pyplot(plt)

        wordcloud_stock()

    with c3:
        mask_3 = filtered_tweets["company"] == options[2]
        filtered_tweets_3 = filtered_tweets.loc[mask_3, :]
        st.metric(
            label=f"Number of tweets for {options[2]}:",
            value=str(filtered_tweets_3.shape[0]),
        )

        # we select all the tweets from 2017 to 2022
        tweet_list = filtered_tweets_3["TweetText"].tolist()
        # join all tweets into a single string
        tweet_string = " ".join(tweet_list)

        # frequency plot
        def frequency_tweets_length_stock():
            sns.set_style("darkgrid")
            sns.displot(filtered_tweets_3["tweet_length"], bins=20)
            plt.title(f"Tweet frequency length for {options[2]}")
            plt.xlabel("Tweet Length")
            plt.ylabel("Number of Tweets")
            plt.show()
            st.pyplot(plt)

        frequency_tweets_length_stock()

        # create the word cloud
        wordcloud = WordCloud(stopwords=stop_words).generate(tweet_string)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.title(f"Wordcloud for {options[2]} from {start_date} to {end_date}")
        plt.axis("off")
        plt.show()

        def wordcloud_stock():
            st.pyplot(plt)

        wordcloud_stock()
