from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from transformers import pipeline
import pandas as pd

import logging
logging.getLogger("py4j").setLevel(logging.ERROR)



"""TODO :
Changer le df et faire un path relative et mettre la data dans son propre dossier  
"""

class PreprocessorPipeline:
    
    def __init__(self, path, output_path):
        self.path = path
        self.output_path = output_path
 
    def import_df(self, path):
        print('Importing the csv')
        spark = SparkSession.builder.appName("CSVtoTable").getOrCreate()

        df = (spark.read.format("csv")
        .option('mode','DROPMALFORMED')
        .options(header = True, inferSchema = True, sep=",",multiLine=True)
        .load(self.path)
        .cache()) # Keep the dataframe in memory for faster processing 
        return df

    def cast_columns(self, df):
        """ Cast good columns types 
        """
        print('Changing the type of columns')
        df = df.select(*[col(c).cast("integer").alias(c) if c in ['ReplyCount','RetweetCount','LikeCount'] else c for c in df.columns])
        df = df.withColumn("PostDate", to_date(df["PostDate"]))
        return df

    def cleaning_tweets(self, df):
        print('Importing the tweets')
        df = df.withColumn("TweetText", trim(regexp_replace("TweetText", "[\n]+", " ")))
        df = df.withColumn("TweetText", trim(regexp_replace("TweetText", "https?://[^ ]+", "")))
        df = df.withColumn("TweetText", trim(regexp_replace("TweetText", "@[^ ]+", "")))
        df = df.withColumn("TweetText", trim(regexp_replace("TweetText", "#[^ ]+", "")))
        df = df.withColumn("TweetText", trim(regexp_replace("TweetText", "[^A-Za-z0-9 ]", "")))
        df = df.withColumn("TweetText", regexp_extract("TweetText", "(2021|2017|2018|2019|2020|2022).*", 0))
        df = df.withColumn("TweetText", regexp_replace("TweetText", "[^a-zA-Z\\s]", ""))

        df = df.na.drop(subset="TweetText") 
        return df

    def dealing_with_na(self, df):
        print('Dealing with na values')
        df = df.na.fill(0, subset=['ReplyCount','RetweetCount','LikeCount'])
        return df

    def loosing_handle(self, df):
        print('Loosing the @ for the handles')
        df = df.withColumn("Handle", trim(regexp_replace("Handle", "@", "")))
        return df

    # def translator(self, df):
    #     # Load pre-trained models for text translation and language detection
    #     translate_model = pipeline('translation', model='t5-base')
    #     detect_lang_model = pipeline('text-classification', model='distilbert-base-multilingual-cased')

    #     # Define a UDF to translate text using the pre-trained models
    #     translate_text_udf = udf(lambda x: translate_text(x))

    #            # function to translate text
    #     def translate_text(text_to_translate):
    #          # Detect the source language of the text
    #         src_lang = detect_lang_model(text_to_translate)[0]['label']
    #         # Translate the text
    #         return translate_model(text_to_translate, src_lang=src_lang, tgt_lang='en')[0]['generated_text']

    #     # Use the UDF to add a new column with the translations
    #     df = df.withColumn("translated_text", translate_text_udf("TweetText"))
    #     return df

    def creating_csv(self, df, output_path):
        print('Creating the cleaned csv!')
        df.write.format("csv").mode("overwrite").save(self.output_path)
        return df


if __name__ == "__main__":
    path = "/Users/sarrabenyahia/Documents/GitHub/NLP_stocks/Data/webscraped_VALERO_ENERGY_CORP.csv"
    output_path = "/Users/sarrabenyahia/Documents/GitHub/NLP_stocks/Data/processed_df.csv"
    preprocessing = PreprocessorPipeline(path =path, output_path=output_path)
    df = preprocessing.import_df(path)
    df = preprocessing.cast_columns(df)
    df = preprocessing.cleaning_tweets(df)
    df = preprocessing.dealing_with_na(df)
    df = preprocessing.loosing_handle(df)
    df = preprocessing.translator(df)
    preprocessing.creating_csv(df, output_path)
    print("Here is the result :) ")
    df.show()