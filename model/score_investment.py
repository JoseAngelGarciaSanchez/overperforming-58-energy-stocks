import pandas as pd
import numpy as np
np.random.seed(42)  # Pour la reproductibilité
pd.options.mode.chained_assignment = None 
class PortfolioModel:
    def __init__(self, path: str, returns_path: str) -> None:
        self.path = path
        self.returns_path = returns_path

    def read_data(self):
        self.returns = pd.read_excel(
            self.returns_path, sheet_name="Returns", header=[5, 6]
        ).T.iloc[2:, :]
        self.df = pd.read_csv(self.path)

    def formatting(self) -> None:
        """Formatting the dates and encoding sentiment columns positive or bullish -> 1, negative or bearish -> -1, neutral -> 0"""

        self.df["PostDate"] = self.df["PostDate"].astype(str).apply(lambda x: x[:-3])
        self.df["PostDate"] = pd.to_datetime(self.df["PostDate"])

        # drop rows with NaN values in the "PostDate" column
        self.df.dropna(subset=["PostDate"], inplace=True)
    
        # add a column for the year and month
        self.df["year"] = self.df["PostDate"].dt.year
        self.df["month"] = self.df["PostDate"].dt.month

        # formatting sentiments
        self.df["sentiment"] = self.df["sentiment"].map({"Bullish": 1, "Bearish": -1})
        self.df["sentiment_base"] = self.df["sentiment_base"].map(
            {"positive": 1, "neutral": 0, "negative": -1}
        )

        # formatting returns
        self.returns = self.returns.rename(columns=self.returns.iloc[0])
        self.returns = self.returns.iloc[2:]
        upercase = lambda x: str(x).upper()
        self.returns.rename(upercase, axis="columns", inplace=True)
        self.returns.reset_index(inplace=True)
        self.returns.rename(
            columns={"level_0": "DATE1", "level_1": "DATE"}, inplace=True
        )
        self.returns.drop(columns="DATE1", inplace=True)
        self.returns["DATE"] = pd.to_datetime(self.returns["DATE"]).dt.date

        # we apply to convert the percentage on indices
        except_column = "DATE"
        selected_columns = [col for col in self.returns.columns if col != except_column]
        result = self.returns[selected_columns].apply(lambda x: x / 100 + 1, axis=1)
        self.returns = pd.concat([self.returns[except_column], result], axis=1)
        self.returns["DATE"] = pd.to_datetime(self.returns["DATE"])
        self.returns["year"] = self.returns["DATE"].dt.year
        self.returns["month"] = self.returns["DATE"].dt.month
        self.returns["yearmonth"] = (
            self.returns["year"].astype(str)
            + "-"
            + self.returns["month"].astype(str).str.zfill(2)
        )
        result_on_pct = self.returns[selected_columns].apply(lambda x: x / 100, axis=1)
        self.returns_on_pct = pd.concat([self.returns[except_column], result_on_pct], axis=1)
        self.returns_on_pct["DATE"] = pd.to_datetime(self.returns["DATE"])
        self.returns_on_pct["year"] = self.returns_on_pct["DATE"].dt.year
        self.returns_on_pct["month"] = self.returns_on_pct["DATE"].dt.month
        self.returns_on_pct["yearmonth"] = (
            self.returns_on_pct["year"].astype(str)
            + "-"
            + self.returns_on_pct["month"].astype(str).str.zfill(2)
        )

     

    def positive_ratio(self) -> pd.DataFrame:
        # group the data by year and month
        grouped = self.df.groupby(["year", "month", "company"])

        # count the number of positive and negative tweets for each year and month
        sentiment_positive_tweets_by_month = grouped["sentiment"].apply(
            lambda x: (x == 1).sum()
        )
        sentiment_negative_tweets_by_month = grouped["sentiment"].apply(
            lambda x: (x == -1).sum()
        )
        sentiment_base_positive_tweets_by_month = grouped["sentiment_base"].apply(
            lambda x: (x == 1).sum()
        )
        sentiment_base_neutral_tweets_by_month = grouped["sentiment_base"].apply(
            lambda x: (x == 0).sum()
        )
        sentiment_base_negative_tweets_by_month = grouped["sentiment_base"].apply(
            lambda x: (x == -1).sum()
        )

        # calculate the ratio of positive and negative tweets for each year and month
        positive_ratios_by_month = (
            sentiment_base_positive_tweets_by_month + sentiment_positive_tweets_by_month
        ) / (
            sentiment_positive_tweets_by_month
            + sentiment_negative_tweets_by_month
            + sentiment_base_positive_tweets_by_month
            + sentiment_base_neutral_tweets_by_month
            + sentiment_base_negative_tweets_by_month
        )

        # formatting
        positive_ratios_by_month = positive_ratios_by_month.reset_index()
        positive_ratios_by_month.rename(columns={0: "positive_ratio"}, inplace=True)
        positive_ratios_by_month["yearmonth"] = (
            positive_ratios_by_month["year"].astype(str)
            + "-"
            + positive_ratios_by_month["month"].astype(str).str.zfill(2)
        )
        return positive_ratios_by_month

    def short_or_long(self):
        """new dataframe with buy or sell at t"""
        positive_ratios_by_month = self.positive_ratio()
        date_index = positive_ratios_by_month["yearmonth"].unique().tolist()
        unique_companies = positive_ratios_by_month["company"].unique().tolist()
        self.shortlongdf = pd.DataFrame(index=date_index)
        for company in unique_companies:
            # selection of the company
            mask = positive_ratios_by_month["company"] == company
            stock_ratios = positive_ratios_by_month.loc[mask]
            # selection of the period
            stock_ratios.loc[:, "positive_ratio_shifted"] = stock_ratios[
                "positive_ratio"
            ].shift(1)
            stock_ratios.loc[:, "buy_or_sell"] = (
                stock_ratios["positive_ratio_shifted"] - 0.5
            ) * 2
            stock_ratios.set_index("yearmonth", inplace=True) # STOCK_RATIONS BETWEEN -1 and 1

            self.stock_ratios = stock_ratios
            # saving info in a dataframe
            self.shortlongdf[company] = stock_ratios["buy_or_sell"]


    """ 
    Pseudo-code : 
    GPT

    Votre description suggère une stratégie d'évaluation de performance pour un modèle d'investissement basé sur l'analyse sentimentale, où la décision d'acheter ou de vendre est prise non seulement sur la base du sentiment actuel ou passé, mais aussi en tenant compte de la performance réelle du titre. Voici comment cette stratégie peut être structurée et implémentée en pseudocode, avant de passer au code Python :
    Pseudocode

        Calculer le signal d'achat ou de vente :
            Utiliser le sentiment du mois précédent (N-1) pour générer un signal d'achat ou de vente.

        Vérifier la performance réelle du titre :
            Si le modèle propose d'acheter (signal > 0), alors vérifier la performance réelle du titre.
                Pour vérifier la performance, comparer le prix du titre au temps t avec son prix au temps t-1 (le mois précédent).
                Si la différence de prix (prix_t - prix_t-1) est positive, alors la performance est jugée positive et le modèle est considéré comme bon pour cette période.
                Sinon, si la différence de prix est négative, la performance est jugée négative et le modèle n'est pas considéré comme bon pour cette période.

        Évaluer la performance du modèle :
            Répéter ce processus pour chaque période et chaque titre concerné.
            Calculer le pourcentage de fois où le modèle a correctement prédit une performance positive lorsque un signal d'achat était donné.


    """
    def calculating_stock(self):
        """ we calcule for each stock the returns and the stock at t: we are going to use self.returns and self.shortlongdf"""

        self.shortlongdf.fillna(0, inplace=True)


    def mapping(self):
        """cumsum for all stocks"""
        self.df_columns_list = [
            "BP PLC",
            "FMC CORP",
            "WEYERHAEUSER CO",
            "ALTAGAS LTD",
            "BHP GROUP",
            "INTERNATIONAL PAPER CO",
            "S&P 500 ENERGY INDEX",
            "STORA ENSO",
            "WILMAR INTERNATIONAL LTD",
            "TOTALENERGIES SE",
        ]

        self.stocklist = [
            "BP/ LN EQUITY",
            "FMC US EQUITY",
            "WY US EQUITY",
            "ALA CT EQUITY",
            "BHP US EQUITY",
            "IP US EQUITY",
            "S5ENRS EQUITY",
            "STERV FH EQUITY",
            "WIL SP EQUITY",
            "TTE FP EQUITY",
        ]

        self.search_dictio = {}
        for i, k in enumerate(self.df_columns_list):
            self.search_dictio[self.stocklist[i]] = k


    def adjust_returns_with_company_names(self):
        # Create a DataFrame to hold adjusted returns, matching the structure of shortlongdf
        adjusted_returns = pd.DataFrame()
        #print(self.returns)
        # Map each company in the dictionary to its corresponding returns in self.returns
        for equity_name, company_name in self.search_dictio.items():
            if equity_name in self.returns.columns:
                # Extract the returns for the specific equity and map it to the company name
                adjusted_returns[company_name] = self.returns[equity_name]
    

        # Ensure the DATE column is available for merging
        adjusted_returns['DATE'] = self.returns.index
        adjusted_returns['year'] = self.returns['year']
        adjusted_returns['month'] = self.returns['month']
        adjusted_returns['yearmonth'] = self.returns['year'].astype(str) + '-' + self.returns['month'].astype(str).str.zfill(2)

        # Reset index to ensure 'yearmonth' can be used for merging
        self.adjusted_returns = adjusted_returns.reset_index(drop=True).set_index('yearmonth')

    def evaluate_model_accuracy(self):
        self.adjusted_returns.index = pd.to_datetime(self.adjusted_returns.index)
        self.shortlongdf.index = pd.to_datetime(self.shortlongdf.index)
        
        # Step 2 & 3: Merge and evaluate
        evaluation_df = self.shortlongdf.join(self.adjusted_returns, how='inner', lsuffix='_buysell', rsuffix='_market')
        
        # Initialize a dictionary to track accuracy metrics for each stock
        accuracy_metrics = {}

        # Function to determine if the prediction matches the market performance
        def prediction_matches(signal, market_return):
            if signal > 0 and market_return > 1:
                return True
            elif signal < 0 and market_return < 1:
                return True
            elif -0.1 < signal < 0.1 and 0.9 < market_return < 1.1:
                return True
            else:
                return False

        # Iterate over each row of the DataFrame
        for index, row in evaluation_df.iterrows():
            # Iterate over each stock's signal column
            for column in evaluation_df.columns:
                if '_buysell' in column:
                    company_name = column.split('_buysell')[0]
                    market_column = company_name + '_market'
                    
                    if market_column in evaluation_df.columns:
                        # Initialize the stock in the dictionary if not already present
                        if company_name not in accuracy_metrics:
                            accuracy_metrics[company_name] = {'correct_predictions': 0, 'total_signals': 0}
                        
                        # Increment total_signals counter for the stock
                        accuracy_metrics[company_name]['total_signals'] += 1
                        
                        # Check if the prediction matches the actual market performance
                        if prediction_matches(row[column], row[market_column]):
                            accuracy_metrics[company_name]['correct_predictions'] += 1

        # Print the accuracy for each stock
        for stock, metrics in accuracy_metrics.items():
            stock_accuracy = (metrics['correct_predictions'] / metrics['total_signals']) * 100 if metrics['total_signals'] > 0 else 0
            print(f'{stock} Accuracy: {stock_accuracy:.2f}%')


    def compute_signal_market_correlation(self):
        self.adjusted_returns.index = pd.to_datetime(self.adjusted_returns.index)
        self.shortlongdf.index = pd.to_datetime(self.shortlongdf.index)
        
        # Step 2: Merge data for correlation analysis
        evaluation_df = self.shortlongdf.join(self.adjusted_returns, how='inner', lsuffix='_signal', rsuffix='_market')
        evaluation_df.to_excel("output.xlsx", index=False)

        # Dictionary to store correlation results
        correlation_results = {}

        # Iterate over each stock to calculate correlation
        for column in self.shortlongdf.columns:
            if '_signal' in column:
                print(column)
                # Extract the company name to match with its market return column
                company_name = column.split('_signal')[0]
                market_column = f'{company_name}_market'
                
                
                # Check if the corresponding market return column exists
                if market_column in evaluation_df.columns:
                    # Calculate correlation
                    correlation = evaluation_df[[column, market_column]].corr().iloc[0, 1]
                    correlation_results[company_name] = correlation

        # Print or return the correlation results
        for stock, correlation in correlation_results.items():
            print(f'{stock} Signal-Market Correlation: {correlation:.4f}')

        # Optionally, return the correlation results if needed for further analysis
        return correlation_results
    
    def launch(self):
        # reading returns and analyse data NLP
        self.read_data()
        # formatting the data
        self.formatting()
        # returning a dataframe with sentiment score stocks by date
        self.short_or_long()
        self.mapping()
        self.adjust_returns_with_company_names()
        self.evaluate_model_accuracy()
        self.compute_signal_market_correlation()
        #self.results_per_stock()


if __name__ == "__main__":
    path = "./../data/data_model/all_data.csv"
    returns_path = "./../data/stocks_data.xlsx"
    model = PortfolioModel(path=path, returns_path=returns_path).launch()