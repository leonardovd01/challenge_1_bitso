import os
import time
from datetime import datetime

import requests
import pandas as pd


def fetch_orderbook(book: list):
    """
    Fetch order book from the bitso API.

    Args:
        book (list): List of book to call from bitso app

    Returns:
        json: Response of bitso API
    """
    url = f"https://api.bitso.com/v3/order_book/?book={book}"
    response = requests.get(url)
    data = response.json()
    return data


def calculate_spread(bid, ask):
    """
    Calculate the spread between bid and ask prices.

    Args:
        bid (float): Bid price.
        ask (float): Ask price.

    Returns:
        float: The calculated spread.
    """    
    spread = (ask - bid) * 100 / ask
    return spread


def main(iterations=None):
    """
    Main function to get spread from the called parameters.
    Continuously fetches order book data and calculates the spread,
    storing the results in a CSV file every 10 minutes.

    Args:
        iterations (int, optional): Number of iterations to run the loop for testing.
    """    
    books = ["btc_mxn", "usd_mxn"]
    observations = []
    iteration_count = 0

    while True:
        for book in books:
            data = fetch_orderbook(book)
            data = data.get('payload')
            timestamp = data.get('updated_at')
            bid = float(data.get('bids')[0].get('price'))
            ask = float(data.get('asks')[0].get('price'))
            spread = calculate_spread(bid, ask)

            # Generate a clean dictionary for appending and creating a DataFrame
            record = {
                "orderbook_timestamp": timestamp,
                "book": book,
                "bid": bid,
                "ask": ask,
                "spread": spread
            }
            observations.append(record)

        # Sleep for 1 second
        time.sleep(1)
        iteration_count += 1

        # Save observations to a file every 10 minutes
        if len(observations) >= 600:  
            df = pd.DataFrame(observations)
            current_time = datetime.utcnow()
            year = current_time.strftime("%Y")
            month = current_time.strftime("%m")
            day = current_time.strftime("%d")
            hour = current_time.strftime("%H")
            minute = current_time.strftime("%M%S")
            
            # Define the partition structure for saving data following Hadoop best practices
            directory = f"data/YEAR={year}/MONTH={month}/DAY={day}/HOUR={hour}"
            os.makedirs(directory, exist_ok=True)

            file_path = f"{directory}/{minute}_orderbook.csv"
            df.to_csv(file_path, index=False)
            print(f'File saved in {file_path}')
            # Reset observations to start fresh every 10 minutes
            observations = []
        if iterations and iteration_count >= iterations:
            break
       

if __name__ == "__main__":
    main()