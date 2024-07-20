import os
import requests
import time
import json
from datetime import datetime
import certifi
import pandas as pd


def fetch_orderbook(book: list):
    """_summary_

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
    """_summary_

    Args:
        bid (_type_): _description_
        ask (_type_): _description_

    Returns:
        _type_: _description_
    """    
    spread = (ask - bid) * 100 / ask
    return spread


def main():
    """Main function to get spred from the called parameters
    """    
    books = ["btc_mxn", "usd_mxn"]
    observations = []

    while True:
        for book in books:
            data = fetch_orderbook(book)
            data = data.get('payload')
            timestamp = data.get('updated_at')
            bid = float(data.get('bids')[0].get('price'))
            ask = float(data.get('asks')[0].get('price'))
            spread = calculate_spread(bid, ask)

            # Generate clean dictionary to append and get dataframe
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

        # Every 10 minutes, save observations to a file
        if len(observations) >= 10:  
            df = pd.DataFrame(observations)
            current_time = datetime.utcnow()
            year = current_time.strftime("%Y")
            month = current_time.strftime("%m")
            day = current_time.strftime("%d")
            hour = current_time.strftime("%H")
            minute = current_time.strftime("%M%S")
            
            # Define the partion to save the data following Hadopp style
            directory = f"data/YEAR={year}/MONTH={month}/DAY={day}/HOUR={hour}"
            os.makedirs(directory, exist_ok=True)

            file_path = f"{directory}/{minute}_orderbook.csv"
            df.to_csv(file_path, index=False)
            print(f'File saved in {file_path}')
            # Reset observations to save new data every ten minutes
            observations = []

if __name__ == "__main__":
    main()