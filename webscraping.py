from bs4 import BeautifulSoup
import requests

def scrapingData():

    # URL of the Wikipedia page
    url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue'

    # Send a GET request to the website
    response = requests.get(url)
    # Convert the html into a format so it can be easier to search for elements
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the table with the class "wikitable"
    #tables = soup.find_all('table', {'class': 'wikitable'})

    tables = soup.find_all('table', {'class': 'wikitable'})


    companies = []

    if tables:
        target_table = tables[0]
        #Extracting rows
        rows = target_table.find_all('tr')
        
          #Start looking at the data after the first index
        for element in rows[1:]:
            #Extracting data from cells
            cells = element.find_all('td')
            #checks that each row has atleast 5 data cells
            if len(cells) >= 5:
                companies_data = {
                    #.text removes the html tags
                    "Company Name" : cells[0].text.strip(),
                    "Industry" : cells[1].text.strip(),
                    "Revenue (USD Millions)" : cells[2].text.strip(),
                    "Profit (USD Millions)" : cells[3].text.strip(),
                    "Number of Employees" : cells[4].text.strip(),
                    "Headquarters" : cells[5].text.strip()
                }
                companies.append(companies_data)

    return companies
    # count = 1
    # for element in companies:
    #     print("\n")
    #     print(f'{count}. {element}')
    #     count += 1
                
    # print(companies[0]['Industry'])

