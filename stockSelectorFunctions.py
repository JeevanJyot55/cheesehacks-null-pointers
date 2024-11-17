import yfinance as yf
import pandas as pd
from tqdm import tqdm

def get_sector(symbol):
    """
    Fetches the sector of a stock using yfinance.
    Args:
        symbol (str): Stock ticker symbol.
    Returns:
        str: Sector of the stock.
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return info.get('sector', 'Unknown')
    except Exception as e:
        print(f"Error fetching sector for {symbol}: {e}")
        return "Unknown"

def get_latest_prices(symbols):
    """
    Fetches the latest closing prices for multiple stocks using yfinance.
    Args:
        symbols (list): List of stock ticker symbols.
    Returns:
        dict: A dictionary with symbols as keys and their latest prices as values.
    """
    try:
        stock_data = yf.download(symbols, period="1d", progress=False)
        if stock_data.empty:
            print("No price data found for the provided symbols.")
            return {}

        # Extract closing prices
        close_prices = stock_data['Close'].iloc[-1]
        return close_prices.to_dict()
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return {}

def calculate_quantity(budget, price):
    """
    Calculates the number of shares that can be purchased within a budget.
    Args:
        budget (float): Total budget.
        price (float): Price per share.
    Returns:
        int: Number of shares that can be purchased.
    """
    if price == "N/A" or price <= 0:
        return 0
    return int(budget // price)  # Floor division to ensure whole numbers

def diversify_and_allocate(mid_cap_csv, sp500_csv, total_budget, mid_cap_percentage, sector_allocation):
    """
    Allocates stocks from mid-cap and S&P 500 based on the percentage split and sector diversification.
    Args:
        mid_cap_csv (str): Path to the mid-cap CSV file.
        sp500_csv (str): Path to the S&P 500 CSV file.
        total_budget (float): Total budget for investments.
        mid_cap_percentage (float): Percentage of stocks from mid-cap (0-100).
        sector_allocation (dict): Sector allocation for diversification.
    """
    try:
        # Load the CSV files
        mid_cap_data = pd.read_csv(mid_cap_csv)
        sp500_data = pd.read_csv(sp500_csv)

        # Ensure required columns exist for S&P 500
        if 'Symbol' not in sp500_data.columns or 'Sector' not in sp500_data.columns:
            print("Error: S&P 500 CSV must contain 'Symbol' and 'Sector' columns.")
            return

        # Fetch sector information dynamically for mid-cap stocks
        print("Fetching sector information for mid-cap stocks...")
        mid_cap_data['Sector'] = mid_cap_data['Symbol'].apply(get_sector)

        # Fetch prices for all stocks
        all_symbols = list(mid_cap_data['Symbol']) + list(sp500_data['Symbol'])
        print("Fetching prices for all stocks...")
        prices = get_latest_prices(all_symbols)

        # Add prices to the DataFrames
        mid_cap_data['Price'] = mid_cap_data['Symbol'].map(prices)
        sp500_data['Price'] = sp500_data['Symbol'].map(prices)

        # Drop rows where price is missing
        mid_cap_data = mid_cap_data.dropna(subset=['Price'])
        sp500_data = sp500_data.dropna(subset=['Price'])

        # Calculate budget allocation
        mid_cap_budget = total_budget * (mid_cap_percentage / 100)
        sp500_budget = total_budget - mid_cap_budget

        print(f"\nAllocating ${mid_cap_budget:.2f} to mid-cap stocks.")
        print(f"Allocating ${sp500_budget:.2f} to S&P 500 stocks.")

        # Diversify by sector for mid-cap stocks
        results = []
        remaining_budget = total_budget

        for sector, allocation in sector_allocation.items():
            sector_budget = mid_cap_budget * allocation
            sector_stocks = mid_cap_data[mid_cap_data['Sector'] == sector]

            print(f"\nAllocating ${sector_budget:.2f} to {sector} sector (mid-cap).")
            for _, row in tqdm(sector_stocks.iterrows(), total=len(sector_stocks), desc=f"Processing {sector} Sector"):
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
                        "Quantity": quantity,
                        "Remaining Budget": round(remaining_budget, 2)
                    })
                if remaining_budget <= 0:
                    print("\nBudget fully utilized.")
                    break
            if remaining_budget <= 0:
                break

        # If budget remains, allocate to S&P 500
        if remaining_budget > 0:
            print("\nSwitching to S&P 500 stocks.")
            for sector, allocation in sector_allocation.items():
                sector_budget = sp500_budget * allocation
                sector_stocks = sp500_data[sp500_data['Sector'] == sector]

                print(f"\nAllocating ${sector_budget:.2f} to {sector} sector (S&P 500).")
                for _, row in tqdm(sector_stocks.iterrows(), total=len(sector_stocks), desc=f"Processing {sector} Sector"):
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
                            "Quantity": quantity,
                            "Remaining Budget": round(remaining_budget, 2)
                        })
                    if remaining_budget <= 0:
                        print("\nBudget fully utilized.")
                        break
                if remaining_budget <= 0:
                    break

        # Convert results to DataFrame and display
        results_df = pd.DataFrame(results)
        print(results_df)

    except Exception as e:
        print(f"Error allocating stocks: {e}")

def main():
    # File paths
    mid_cap_csv = './mid-cap.csv'
    sp500_csv = './s&p500.csv'

    # Input total budget
    try:
        total_budget = float(input("Enter your total budget for investment (e.g., 10000): "))
    except ValueError:
        print("Invalid budget. Please enter a numeric value.")
        return

    # Input mid-cap percentage
    try:
        mid_cap_percentage = float(input("Enter the percentage of mid-cap allocation (0-100): "))
        if not (0 <= mid_cap_percentage <= 100):
            print("Percentage must be between 0 and 100.")
            return
    except ValueError:
        print("Invalid percentage. Please enter a numeric value between 0 and 100.")
        return

    # Define sector allocation (adjust percentages as needed)
    sector_allocation = {
        "Technology": 0.4,  # 40% of mid-cap budget
        "Healthcare": 0.3,  # 30% of mid-cap budget
        "Consumer Goods": 0.2,  # 20% of mid-cap budget
        "Energy": 0.1         # 10% of mid-cap budget
    }

    # Allocate stocks
    diversify_and_allocate(mid_cap_csv, sp500_csv, total_budget, mid_cap_percentage, sector_allocation)

if __name__ == "__main__":
    main()
