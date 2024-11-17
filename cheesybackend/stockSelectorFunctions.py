from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
from tqdm import tqdm

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend-backend communication

def get_sector(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return info.get('sector', 'Unknown')
    except Exception as e:
        print(f"Error fetching sector for {symbol}: {e}")
        return "Unknown"

def get_latest_prices(symbols):
    try:
        stock_data = yf.download(symbols, period="1d", progress=False)
        if stock_data.empty:
            print("No price data found for the provided symbols.")
            return {}

        close_prices = stock_data['Close'].iloc[-1]
        return close_prices.to_dict()
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return {}

def calculate_quantity(budget, price):
    if price == "N/A" or price <= 0:
        return 0
    return int(budget // price)

def diversify_and_allocate(mid_cap_csv, sp500_csv, total_budget, mid_cap_percentage, sector_allocation):
    try:
        mid_cap_data = pd.read_csv(mid_cap_csv)
        sp500_data = pd.read_csv(sp500_csv)

        if 'Symbol' not in sp500_data.columns or 'Sector' not in sp500_data.columns:
            return {"error": "S&P 500 CSV must contain 'Symbol' and 'Sector' columns."}

        print("Fetching sector information for mid-cap stocks...")
        mid_cap_data['Sector'] = mid_cap_data['Symbol'].apply(get_sector)

        all_symbols = list(mid_cap_data['Symbol']) + list(sp500_data['Symbol'])
        print("Fetching prices for all stocks...")
        prices = get_latest_prices(all_symbols)

        mid_cap_data['Price'] = mid_cap_data['Symbol'].map(prices)
        sp500_data['Price'] = sp500_data['Symbol'].map(prices)

        mid_cap_data = mid_cap_data.dropna(subset=['Price'])
        sp500_data = sp500_data.dropna(subset=['Price'])

        mid_cap_budget = total_budget * (mid_cap_percentage / 100)
        sp500_budget = total_budget - mid_cap_budget

        results = []
        remaining_budget = total_budget

        for sector, allocation in sector_allocation.items():
            sector_budget = mid_cap_budget * allocation
            sector_stocks = mid_cap_data[mid_cap_data['Sector'] == sector]

            for _, row in tqdm(sector_stocks.iterrows(), total=len(sector_stocks)):
                symbol, price = row['Symbol'], row['Price']
                quantity = calculate_quantity(sector_budget, price)
                if quantity > 0:
                    sector_budget -= quantity * price
                    remaining_budget -= quantity * price
                    results.append({
                        "Category": "Mid Cap",
                        "Sector": sector,
                        "Symbol": symbol,
                        "Price": round(price, 2),
                        "Quantity": quantity
                    })
                if remaining_budget <= 0:
                    break
            if remaining_budget <= 0:
                break

        if remaining_budget > 0:
            for sector, allocation in sector_allocation.items():
                sector_budget = sp500_budget * allocation
                sector_stocks = sp500_data[sp500_data['Sector'] == sector]

                for _, row in tqdm(sector_stocks.iterrows(), total=len(sector_stocks)):
                    symbol, price = row['Symbol'], row['Price']
                    quantity = calculate_quantity(sector_budget, price)
                    if quantity > 0:
                        sector_budget -= quantity * price
                        remaining_budget -= quantity * price
                        results.append({
                            "Category": "S&P 500",
                            "Sector": sector,
                            "Symbol": symbol,
                            "Price": round(price, 2),
                            "Quantity": quantity
                        })
                    if remaining_budget <= 0:
                        break
                if remaining_budget <= 0:
                    break

        return results
    except Exception as e:
        print(f"Error allocating stocks: {e}")
        return {"error": str(e)}

@app.route('/allocate', methods=['POST'])
def allocate_stocks():
    try:
        data = request.json
        total_budget = data['budget']
        mid_cap_percentage = data['risk']

        mid_cap_csv = './mid-cap.csv'
        sp500_csv = './s&p500.csv'

        sector_allocation = {
            "Technology": 0.4,
            "Healthcare": 0.3,
            "Consumer Goods": 0.2,
            "Energy": 0.1
        }

        recommendations = diversify_and_allocate(mid_cap_csv, sp500_csv, total_budget, mid_cap_percentage, sector_allocation)

        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
