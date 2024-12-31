# Extract the first table (assuming it's the main one you're interested in)
if tables:
    target_table = tables[0]  # You can select a specific table if needed

    # Extract rows from the table
    rows = target_table.find_all('tr')

    # Initialize lists for extracted data
    company_names = []
    revenues = []

    # Loop through each row
    for row in rows[1:]:  # Skip the header row
        cells = row.find_all('td')
        if len(cells) >= 2:  # Check if the row has enough columns
            company_name = cells[0].text.strip()  # First column is the company name
            revenue = cells[2].text.strip()  # Second column is the revenue
            company_names.append(company_name)
            revenues.append(revenue)

    # Print the extracted data
    for name, revenue in zip(company_names, revenues):
        print(f"Company: {name}, Revenue: {revenue}")
else:
    print("No table found.")




    from webscraping import scrapingData
import pandas as pd

companies = scrapingData()

df = pd.DataFrame(companies)
#print(df)


# count = 1
# for element in companies:
#     print("\n")
#     print(f'{count}. {element}')
#     count += 1

import pandas as pd

# Load the data
df = pd.DataFrame(companies)

# Clean numeric fields
df['Revenue (USD Millions)'] = df['Revenue (USD Millions)'].str.replace('[$,]', '', regex=True).astype(float)
df['Profit (USD Millions)'] = df['Profit (USD Millions)'].str.replace('[$,]', '', regex=True).astype(float)
df['Number of Employees'] = df['Number of Employees'].str.replace(',', '', regex=True).astype(float)

# One-Hot Encoding for categorical features
df = pd.get_dummies(df, columns=['Industry', 'Headquaters'], drop_first=True)

# Drop rows with missing values (if any)
df = df.dropna()


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Features and target
X = df.drop(columns=['Company Name', 'Profit (USD Millions)'])
y = df['Profit (USD Millions)']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")


import matplotlib.pyplot as plt

# Actual vs Predicted Plot
plt.scatter(y_test, y_pred, alpha=0.7)
plt.xlabel("Actual Profit")
plt.ylabel("Predicted Profit")
plt.title("Actual vs Predicted Profit")
plt.show()
