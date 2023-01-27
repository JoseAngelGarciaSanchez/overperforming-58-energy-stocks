from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from transformers import pipeline
import sys

class Model:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("tarnformnet/Stock-Sentiment-BERT")
        self.model = AutoModelForSequenceClassification.from_pretrained("tarnformnet/Stock-Sentiment-BERT",from_tf=True)
        self.nlp = pipeline("sentiment-analysis", model="tarnformnet/Stock-Sentiment-BERT", tokenizer="tarnformnet/Stock-Sentiment-BERT")
        
    def predict(self, dataframe_path: str, output_path: str):
        # Load your dataframe
        df = pd.read_csv(dataframe_path)

        # Using map function
        df["sentiment"] = df["TweetText"].map(lambda x: self.nlp(x)[0]['label'])

        # Save the dataframe with the new column
        df.to_csv(output_path, index=False)


if __name__ == "__main__":

    dataframe_path = sys.argv[1]
    output_path = "/Users/sarrabenyahia/Documents/GitHub/overperforming-58-energy-stocks/model/data.csv"
    model = Model()
    df = model.predict(dataframe_path,output_path)

    print("Here is the result :) ")
    print(df)
