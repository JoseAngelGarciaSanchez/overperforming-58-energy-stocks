from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from langdetect import detect
import nltk
import sys

nltk.download('punkt')
nltk.download('perluniprops')


class PreprocessorPipeline:

    def __init__(self, path, output_path):
        self.path = path
        self.output_path = output_path

    # ajouter une fonction pour concatener les csv?

    def import_df(self, path):
        """ Importing the webscrapped df to preprocess...
        """

        print('---Importing the tweets...')

        spark = SparkSession.builder.appName("CSVtoTable").getOrCreate()

        df = (spark.read.format("csv")
              .option('mode', 'DROPMALFORMED')
              .options(header=True, inferSchema=True, sep=",", multiLine=True)
              .load(self.path)
              .cache())  # Keep the dataframe in memory for faster processing

        return df

    def cast_columns(self, df):
        """ This function casts good columns types : ints and dates
        """
        print('---Changing the type of columns...')

        df = df.select(*[col(c).cast("integer").alias(c) if c in ['ReplyCount',
                       'RetweetCount', 'LikeCount'] else c for c in df.columns])
        df = df.withColumn("PostDate", to_date(df["PostDate"]))

        return df

    def cleaning_tweets(self, df):
        """ In this function, we're cleaning the text of the tweets. We're trimming all the special characters, the links, 
            and keeping only the text part.
        """

        print('---Cleaning the tweets with regex...')

        df = df.withColumn("TweetText", trim(
            regexp_replace("TweetText", "[\n]+", " ")))
        df = df.withColumn("TweetText", trim(
            regexp_replace("TweetText", "https?://[^ ]+", "")))
        df = df.withColumn("TweetText", trim(
            regexp_replace("TweetText", "@[^ ]+", "")))
        df = df.withColumn("TweetText", trim(
            regexp_replace("TweetText", "#[^ ]+", "")))
        df = df.withColumn("TweetText", trim(
            regexp_replace("TweetText", "[^A-Za-z0-9 ]", "")))
        df = df.withColumn("TweetText", regexp_extract(
            "TweetText", "(2021|2017|2018|2019|2020|2022).*", 0))
        df = df.withColumn("TweetText", regexp_replace(
            "TweetText", "[^a-zA-Z\\s]", ""))

        return df

    def dealing_with_na(self, df):
        """ Here, we're dealing with NA values. For the int columns, we're filling the NAs with 0 
            and we're dropping the empty tweets.
        """

        print('---Dealing with na values...')

        df = df.na.fill(0, subset=['ReplyCount', 'RetweetCount', 'LikeCount'])
        df = df.dropna(subset=["TweetText"])

        return df

    def loosing_handle(self, df):
        """ This function looses the @ for the handles.
        """

        print('---Cleaning the handles...')

        df = df.withColumn("Handle", trim(regexp_replace("Handle", "@", "")))

        return df

    def filtering_english(self, df):
        """ This function detects the langage of each tweets and filters 
            only those in english."""

        print('---Choosing only the english tweets...')

        df_pd = df.toPandas()

        def detect_en(text):
            try:
                return detect(text) == 'en'
            except:
                return False
        df_pd = df_pd[df_pd['TweetText'].apply(detect_en)]

        spark = SparkSession.builder.appName("CSVtoTable").getOrCreate()
        df = spark.createDataFrame(df_pd)

        return df

    def creating_csv(self, df):
        """ Creating and saving the cleaned csv"""
        print('---Creating the cleaned csv!')

        df.write.format("csv").mode("overwrite").option(
            "header", "true").save(self.output_path)
        return df


if __name__ == "__main__":

    path = sys.argv[1]
    output_path = "./../data_cleaned/" + path.split("/")[-1]
    preprocessing = PreprocessorPipeline(path=path, output_path=output_path)
    df = preprocessing.import_df(path)
    df = preprocessing.cast_columns(df)
    df = preprocessing.cleaning_tweets(df)
    df = preprocessing.dealing_with_na(df)
    df = preprocessing.loosing_handle(df)
    df = preprocessing.filtering_english(df)
    preprocessing.creating_csv(df)

    print("Here is the result :) ")
    df.show()
