from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd


def get_page(url):
    # Set up the request headers that we're going to use, to simulate
    # a request by the Chrome browser. Simulating a request from a browser
    # is generally good practice when building a scraper
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }

    return requests.get(url, headers=headers)


def parse_rows(table_rows):
    parsed_rows = []

    for table_row in table_rows:
        parsed_row = []
        el = table_row.xpath("./div")

        none_count = 0

        for rs in el:
            try:
                (text,) = rs.xpath('.//span/text()[1]')
                parsed_row.append(text)
            except ValueError:
                parsed_row.append(np.NaN)
                none_count += 1

        if (none_count < 4):
            parsed_rows.append(parsed_row)

    return pd.DataFrame(parsed_rows)


def clean_data(df):
    df = df.set_index(0)  # Set the index to the first column: 'Period Ending'.
    df = df.transpose()  # Transpose the DataFrame, so that our header contains the account names

    # Rename the "Breakdown" column to "Date"
    cols = list(df.columns)
    cols[0] = 'Date'
    df = df.set_axis(cols, axis='columns', inplace=False)

    numeric_columns = list(df.columns)[1::]  # Take all columns, except the first (which is the 'Date' column)

    for column_index in range(1, len(df.columns)):  # Take all columns, except the first (which is the 'Date' column)
        df.iloc[:, column_index] = df.iloc[:, column_index].str.replace(',', '')  # Remove the thousands separator
        df.iloc[:, column_index] = df.iloc[:, column_index].astype(np.float64)  # Convert the column to float64

    return df


def scrape_table(url):
    # Fetch the page that we're going to parse
    page = get_page(url)

    # Parse the page with LXML, so that we can start doing some XPATH queries
    # to extract the data that we want
    tree = html.fromstring(page.content)

    # Fetch all div elements which have class 'D(tbr)'
    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

    # Ensure that some table rows are found; if none are found, then it's possible
    # that Yahoo Finance has changed their page layout, or have detected
    # that you're scraping the page.
    assert len(table_rows) > 0

    df = parse_rows(table_rows)
    df = clean_data(df)

    return df


def get_statement(symbol):
    statement = {}
    statement['balance'] = scrape_table(f'https://finance.yahoo.com/quote/{symbol}/balance-sheet/?p={symbol}')
    statement['income'] = scrape_table(f'https://finance.yahoo.com/quote/{symbol}/financials/?p={symbol}')
    statement['cash'] = scrape_table(f'https://finance.yahoo.com/quote/{symbol}/cash-flow/?p={symbol}')
    statement2 = {}
    for key in statement.keys():
        statement2[key] = {}
        for col in statement[key].columns:
            statement2[key][col] = statement[key][col].to_list()
            if col == 'Date':
                dates = []
                for item in statement2[key]['Date']:
                    if item == 'ttm':
                        value = f"{str(datetime.now().year)}{str(datetime.now().month).zfill(2)}{str(datetime.now().day).zfill(2)}"
                    else:
                        value = item.split('/')[2] + item.split('/')[0].zfill(2) + item.split('/')[1].zfill(2)
                    dates.append(int(value))
                statement2[key]['Date'] = dates

    return statement2