from webscraping import scrapingData
from sklearn.pipeline import Pipeline
# To be able to apply different transformations to different columns
from sklearn.compose import ColumnTransformer
#Convert features into a format that can be provided to machine learning algoithms
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
import pandas as pd


def main():

    companies = scrapingData()

    df = pd.DataFrame(companies)

    # Converting revenue, profit and employees to a numeric type
    # .str - provides access to string manipulation methods
    # Remove any $ or , and replace it with empty string
    # Last convert to int
    df['Revenue (USD Millions)'] = df['Revenue (USD Millions)'].str.replace('[$,]', '', regex=True).astype(int)
    df["Profit (USD Millions)"] = df["Profit (USD Millions)"].str.replace('[$,]', '', regex=True).astype(int)
    df["Number of Employees"] = df["Number of Employees"].str.replace('[$,]', '', regex=True).astype(int)

    # Drop rows with missing values
    df = df.dropna()
    
    # print(df["Revenue (USD Millions)"])
    # print(df["Profit (USD Millions)"])
    # print(df["Number of Employees"])

    X = df[["Industry", "Profit (USD Millions)", "Number of Employees", "Headquarters"]]
    y = df["Revenue (USD Millions)"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown ="ignore"), ["Industry", "Headquarters"]),
            ("num", StandardScaler(), ["Profit (USD Millions)", "Number of Employees"])
        ]
    )

    model = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", LinearRegression)])


if __name__ == "__main__":
    main()



