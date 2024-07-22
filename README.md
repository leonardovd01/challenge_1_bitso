# Challenge 1 SDE Bitso

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Unit Testing](#utest)
- [Partitions Justification](#partitions)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
“Markets team” needs to monitor the bid-ask spread from the “order books” MXN_BTC and USD_MXN, they need to
do custom analysis on the bid-ask spread and create alerts whenever the spread is bigger than 1.0%, 0.5%, 0.1% or
any other custom value in one second observations.
To enable them you need to create a process that gets the order books each second and extract the necessary
values to power the analysis. The process should store a file every 10 min with all the observations gathered (600
records) in that timespan. This file will be stored in the “data lake” and must be partitioned.

The repository uses the [Bitso API](https://api.bitso.com/v3/order_book/?book={book}) to fetch the required information, transform the data, and save it in a structured format that simulates partitioning in an S3 environment.

## Requirements
All the dependencies needed for this project are in the: `requirements.txt` file.

## Installation
Follow these steps to set up and run the project locally:

1. Clone the repository:
    ```bash
    git clone https://github.com/leonardovd01/challenge_1_bitso.git
    ```

2. Navigate to the project directory:
    ```bash
    cd challenge_1_bitso
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
The project includes a script and a Jupyter Notebook that perform the same ETL data processing tasks. You can choose to run either of them based on your preference.

1. **get_spread.py**:
    This script performs the ETL challenge 1 tasks. You can run it using the following command:
    ```bash
    python get_spread.py
    ```

2. **Challenge_1.ipynb**:
    This Jupyter Notebook contains the same analysis and processing steps as the script. To run it, open Jupyter Notebook and navigate to the notebook file:
    ```bash
    jupyter notebook Challenge_1.ipynb
    ```

## Unit Testing

You can find the unit testing code in `test_script.py` and the requirements in `requirements_test.txt`.

## Partitions Justification

### Nested DateTime Partitions
Using a partitioned structure is an effective way to manage large datasets, particularly when dealing with time-series data. This approach is a common best practice in frameworks like Hadoop. The recommended structure involves organizing data hierarchically based on date and time components (year, month, day, hour, etc.). This organization not only improves query efficiency but also simplifies data management tasks such as archiving and purging old data.

Given that files will be deposited every ten minutes, it is advisable to use an hourly granularity data file schema with minutes included in the file names. The recommended partitioning structure is as follows:

- Yearly: year=YYYY
- Monthly: year=YYYY/month=MM
- Daily: year=YYYY/month=MM/day=DD
- Hourly: year=YYYY/month=MM/day=DD/hour=HH

The file name should be formatted as Minute_orderbook.csv.

For an example of this structure, refer to the data folder in this repository.

## Contributing
Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any questions or inquiries, please contact [leonardovd01](https://github.com/leonardovd01).
