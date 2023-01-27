# Overperforming 58 energy stocks

## Introduction 
When rational arbitrageurs have limited risk-bearing capacity and time horizons, the actions of irrational noise traders can affect asset prices (De Long, Shleifer, Summers, & Waldmann, 1990a). Such actions can be interpreted as being driven by fluctuating investor sentiment. This creates the possibility of trading profitably on the basis of investor sentiment, most obviously by being a contrarian, but, under some circumstances, it may be rational to “jump on the bandwagon” and bet with, rather than against, noise traders (De Long, Shleifer, Summers, & Waldmann, 1990b). Various proxies for investor sentiment have been proposed (Baker & Wurgler, 2006), but perhaps the most direct way to measure sentiment in the stock market is to analyze the words of those who are commenting on stocks. One traditional source of such comments is stories in the news media (Tetlock, 2007). More recently, Google searches and Twitter feeds have been used (Mao, Counts, & Bollen, 2015). 

## The project 

This project was carried out as part of an exam-project in the MoSEF Data Science Master of Paris 1 Panthéon Sorbonne. You can find different parts in this repository :

- Webscraping of twitter with selenium
- Cleaning and preprocessing with pyspark
- Exploratory Data Analysis
- Sentiment Analysis modeling
- Streamlit application

All these steps were carried to try to recreate the strategies from the Bloomberg's article ["Embedded value in Bloomberg News & Social Sentiment Data"](https://developer.twitter.com/content/dam/developer-twitter/pdfs-and-files/Bloomberg-Twitter-Data-Research-Report.pdf)

## Getting started 

First, you'll have to clone the repository and activate your virtual environment.
Then,  install the required packages with : 

```
pip install -r requirements.txt
```

### 1. Webscraping Twitter 
You can run the webscrapping with the following command : 

```
python twitter_scrapper.py
```

### 2. Cleaning and preprocessing of the dataset
You can clean your webscrapped dataset with the following command : 

```
python preprocessing.py
```

### 3. EDA
You can see the script for the EDA in the script below : 
```
python A AJOUTER.py
```

### 4. Sentiment Analysis
You can run the model with the following command : 
```
python A AJOUTER.py
```

### 5. Launching the streamlit application
You can run the model with the following command : 

```
streamlit run home.py
```
