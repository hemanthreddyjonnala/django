from django.shortcuts import render
import pandas as pd
from django.views import View
from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt
import os, sys, traceback
from .models import StockTicker
from django.db import connection
from base.views import tables
import time
from django.contrib import messages


query = '''select ticker, pe_ttm,book_price, per_50_mva, per_200_mva, trend, vol_trend, price_per_change, per_day_change, vol_per_change,  price_intraday, previous_close,  market_cap,   per_52_low, per_52_high, target_est_year, eps_ttm, 
 forward_pe, peg_ratio, book_sales, profit_margin, current_ratio, avg_vol_three_month, company_name, sp_500 from stocks_stockticker'''


def get_per_value(val1, val2):
    value = round((float(val1) - float(val2)) * 100 / float(val2), 2)
    return value


def dump_to_db(db_table, stock_screen, app_table):
    model_instances = [db_table(
        ticker=stock_screen[sym]['Ticker'],
        market_cap=stock_screen[sym]['Market Cap'],
        trend=stock_screen[sym]['TREND'],
        sp_500=stock_screen[sym]['SP500'],
        per_day_change=stock_screen[sym]['% Change'],
        previous_close=stock_screen[sym]['Previous Close'],
        volume=stock_screen[sym]['Volume'],
        per_50_mva=stock_screen[sym]['%50MVA'],
        per_200_mva=stock_screen[sym]['%200MVA'],
        per_52_low=stock_screen[sym]['%52LOW'],
        per_52_high=stock_screen[sym]['%52HIGH'],
        target_est_year=round(float(stock_screen[sym]['1y Target Est']), 2),
        eps_ttm=stock_screen[sym]['Diluted EPS (ttm)'],
        pe_ttm=stock_screen[sym]['PE Ratio (TTM)'],
        forward_pe=stock_screen[sym]['Forward P/E 1'],
        peg_ratio=stock_screen[sym]['PEG Ratio (5 yr expected) 1'],
        book_price=stock_screen[sym]['Price/book (mrq)'],
        book_sales=stock_screen[sym]['Price/sales (ttm)'],
        profit_margin=stock_screen[sym]['Profit margin'],
        current_ratio=stock_screen[sym]['Current ratio (mrq)'],
        avg_vol_three_month=stock_screen[sym]['Avg vol (3-month) 3'],
        company_name=stock_screen[sym]['Name'],
        price_intraday=stock_screen[sym]['Price (Intraday)'],
        vol_trend = stock_screen[sym]['VOL_TREND'],
        price_per_change = stock_screen[sym]['price_per_change'],
        vol_per_change = stock_screen[sym]['vol_per_change']
    ) for sym in stock_screen.keys()]

    db_table.objects.all().delete()
    db_table.objects.bulk_create(model_instances)
    data = my_custom_sql(f"{query}")
    return data

def my_custom_sql(query):
    with connection.cursor() as cursor:
        print(query)
        cursor.execute(query)
        data = {}
        data['rows'] = cursor.fetchall()
        data['names'] = []
        for row in data['rows']:
            data['names'] = list(map(lambda x: x[0], cursor.description))
            break

    return data


def get_sub_trend(check_price):
    trend = 0
    per_change = None
    up = False
    def cal_per_change(i, j):
        return round((check_price[i] - check_price[j]) * 100 / check_price[j], 2)
    rows = len(check_price) -1
    for i in range(rows, 1, -1):
        if check_price[i-1] <= check_price[i]:
            up = True
            trend += 1
        else:
            break
    if up:
        per_change = cal_per_change(-1, -(trend+1))

    if not up:
        for i in range(rows, 1, -1):
            if check_price[i - 1] > check_price[i]:
                trend -= 1
            else:
                break
        per_change = cal_per_change(-1, trend-1)
    return trend, per_change


def get_trend(sym, start , now):
    df = pdr.get_data_yahoo(sym, start, now, threads = False)
    check_price = df['Adj Close'].to_list()
    price_trend, price_per_change = get_sub_trend(check_price)
    check_vol = df['Volume'].to_list()
    vol_trend, vol_per_change = get_sub_trend(check_vol)
    return price_trend, vol_trend, price_per_change, vol_per_change


class StocksView(View):
    def get(self, request):
        messages.success(request, 'Please wait')
        yf.pdr_override()
        sp_500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0].filter(
            ['Symbol', 'Security'], axis=1)
        active_df = pd.read_html('https://finance.yahoo.com/most-active')[0]
        active_tickers = active_df['Symbol'].to_list()
        active_df = active_df.set_index('Symbol')
        active_stats = active_df.to_dict()
        stock_stats = {}
        stock_screen = {}
        for row in sp_500.itertuples():
            stock_stats[row[1]] = {}
        # active_tickers = active_tickers[0:5]
        start = dt.datetime.now() - dt.timedelta(days=20)
        now = dt.datetime.now()
        for sym in active_tickers:
            try:
                print(f"Analysis for {sym}")
                # time.sleep(5)
                stock_screen[sym] = {}
                stock_screen[sym]['Name'] = active_stats['Name'][sym]
                stock_screen[sym]['Ticker'] = sym
                stock_screen[sym]['% Change'] = round(float(active_stats['% Change'][sym].replace('%','').replace('+','')),2)
                stock_screen[sym]['Price (Intraday)'] = round(float(active_stats['Price (Intraday)'][sym]),2)
                stock_screen[sym]['Market Cap'] = active_stats['Market Cap'][sym]
                if sym in stock_stats.keys():
                    stock_screen[sym]['SP500'] = 'YES'
                else:
                    stock_screen[sym]['SP500'] = 'NO'

                stock_screen[sym]['TREND'], stock_screen[sym]['VOL_TREND'], stock_screen[sym]['price_per_change'], stock_screen[sym]['vol_per_change'] = get_trend(sym, start, now)

                urls = ['https://sg.finance.yahoo.com/quote/{0}/key-statistics?p={0}',
                        'https://finance.yahoo.com/quote/{0}?p={0}']
                for url in urls:
                    stock_url = url.format(sym)
                    df_list = pd.read_html(stock_url)
                    for df in df_list:
                        for item in df.to_dict('records'):
                            stock_screen[sym][item[0]] = item[1]

                stock_screen[sym]['Volume'] = int(stock_screen[sym]['Volume'])
                stock_screen[sym]['%50MVA'] = get_per_value(stock_screen[sym]['Price (Intraday)'], stock_screen[sym]['50-day moving average 3'])
                stock_screen[sym]['%200MVA'] = get_per_value(stock_screen[sym]['Price (Intraday)'], stock_screen[sym]['200-day moving average 3'])
                stock_screen[sym]['%52LOW'] = get_per_value(stock_screen[sym]['Price (Intraday)'], stock_screen[sym]['52-week low 3'])
                stock_screen[sym]['%52HIGH'] = get_per_value(stock_screen[sym]['Price (Intraday)'], stock_screen[sym]['52-week high 3'])
            except:
                print(f"exception for {sym}")
                print(f"{sys.exc_info()[0]},{sys.exc_info()[1]},{traceback.format_tb(sys.exc_info()[2])} ")
                del stock_screen[sym]
                continue

        return render(request, 'stocks/active.html', dump_to_db(StockTicker, stock_screen, "stocks_stockticker"))


def get_most_active(request):
    messages.success(request, 'Latest Results')
    data =my_custom_sql(query)
    data['tables'] = tables
    return render(request, 'stocks/active.html', data)


def get_query_results(request):
    data = my_custom_sql(f'''{request.POST["stocks-search-query"]}''')
    data['tables'] = tables
    return render(request, 'stocks/active.html', data)

