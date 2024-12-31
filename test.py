from bs4 import BeautifulSoup
import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def scrapingData():
    # URL of the Wikipedia page
    url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue'

    # Send a GET request to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the table with the class "wikitable"
    tables = soup.find_all('table', {'class': 'wikitable'})

    companies = []

    if tables:
        target_table = tables[0]
        # Extracting rows
        rows = target_table.find_all('tr')
        
        # Start looking at the data after the first index
        for element in rows[1:]:
            # Extracting data from cells
            cells = element.find_all('td')
            # Checks that each row has at least 5 data cells
            if len(cells) >= 5:
                companies_data = {
                    # .text removes the HTML tags
                    "Company Name": cells[0].text.strip(),
                    "Industry": cells[1].text.strip(),
                    "Revenue (USD Millions)": cells[2].text.strip().replace('$', '').replace(',', ''),
                    "Profit (USD Millions)": cells[3].text.strip().replace('$', '').replace(',', ''),
                    "Number of Employees": cells[4].text.strip().replace(',', ''),
                    "Headquarters": cells[5].text.strip()
                }
                companies.append(companies_data)

    return companies

def main():
    # Scrape data
    companies = scrapingData()

    # Convert scraped data to DataFrame
    df = pd.DataFrame(companies)

    # Convert columns to numeric where applicable
    df["Revenue (USD Millions)"] = pd.to_numeric(df["Revenue (USD Millions)"], errors='coerce')
    df["Profit (USD Millions)"] = pd.to_numeric(df["Profit (USD Millions)"], errors='coerce')
    df["Number of Employees"] = pd.to_numeric(df["Number of Employees"], errors='coerce')

    # Drop rows with missing values
    df = df.dropna()

    # Features and target
    X = df[["Industry", "Profit (USD Millions)", "Number of Employees", "Headquarters"]]
    y = df["Revenue (USD Millions)"]

    # Preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["Industry", "Headquarters"]),
            ("num", StandardScaler(), ["Profit (USD Millions)", "Number of Employees"])
        ]
    )

    # Model pipeline
    model = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", LinearRegression())])

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Predict for a specific company
    new_company = pd.DataFrame({
        "Industry": ["Retail"],
        "Profit (USD Millions)": [30000],
        "Number of Employees": [150000],
        "Headquarters": ["United States"]
    })

    prediction = model.predict(new_company)
    print(f"Predicted Revenue (USD Millions) for the company: {prediction[0]:.2f}")

if __name__ == "__main__":
    main()