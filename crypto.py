import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Send a request to CoinMarketCap
url = "https://coinmarketcap.com/"
response = requests.get(url)
response.raise_for_status()  # Check for request errors

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Step 3: Extract data
data = []
table_rows = soup.find_all('tr')

for row in table_rows[1:]:
    columns = row.find_all('td')
    
    # Check if the row has enough columns
    if len(columns) < 11:
        continue  # Skip rows with missing data
    
    try:
        name = columns[2].text.strip()  # Name of the cryptocurrency
        price = columns[3].text.strip()  # Current price
        market_cap = columns[7].text.strip()  # Market cap
        volume_24h = columns[8].text.strip()  # 24h volume
        change_7d = columns[10].text.strip()  # 7-day change

        data.append([name, price, market_cap, volume_24h, change_7d])
    except IndexError:
        print("Skipping row due to missing data.")
        continue

# Step 4: Convert to a pandas DataFrame
df = pd.DataFrame(data, columns=['Name', 'Price', 'Market Cap', '24h Volume', '7d Change'])
print(df.head())

# Step 5: Save the data to a CSV file (optional)
df.to_csv('cryptocurrency_data.csv', index=False)
print("Data saved to cryptocurrency_data.csv")
