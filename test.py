from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

def fetch_52_week_highs():
    url = 'https://www.barchart.com/stocks/highs-lows/highs?timeFrame=1y'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Update the path to your ChromeDriver binary
    service = Service('/path/to/chromedriver')  # Adjust the path

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    try:
        # Wait for the table to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'bc-table-scrollable-inner'))
        )
        time.sleep(5)  # Additional wait to ensure content is fully loaded

        # Get page source after JavaScript has executed
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', {'class': 'bc-table-scrollable-inner'})
        if table:
            rows = table.find_all('tr')[1:]  # Skip header row
            stocks = []
            for row in rows:
                cols = row.find_all('td')
                if len(cols) > 1:
                    symbol = cols[0].text.strip()
                    name = cols[1].text.strip()
                    stocks.append({'symbol': symbol, 'name': name})
            return stocks
        else:
            print("Error: Unable to find the data table on the page.")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        driver.quit()

def save_to_csv(stocks, filename='52_week_highs.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['symbol', 'name'])
        writer.writeheader()
        for stock in stocks:
            writer.writerow(stock)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    stocks = fetch_52_week_highs()
    if stocks:
        save_to_csv(stocks)
    else:
        print("No data retrieved.")
