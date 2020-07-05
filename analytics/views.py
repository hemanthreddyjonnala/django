from django.http import JsonResponse
from django.shortcuts import render
from stocks.models import StockTicker
from django.core import serializers
from analytics.models import PriceInfo
from stocks.views import my_custom_sql
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf
from django.http import JsonResponse
from stocks.views import dump_to_db
from analytics import statements


def get_price_data(ticker, days, sample, span1, span2):
    start = dt.datetime.now() - dt.timedelta(days=days)
    now = dt.datetime.now()
    df = pdr.get_data_yahoo(ticker, start, now)
    # df =df.sample(n=int(len(df)/sample))
    df = df.iloc[::sample]
    df['EMA1'] = df['Adj Close'].ewm(span=span1, adjust=False).mean()
    df['EMA2'] = df['Adj Close'].ewm(span=span2, adjust=False).mean()
    # data = df.to_dict(orient='records')
    data ={'labels':[],'data':[], 'Adj_close':[], 'Open': [], 'EMA1':[], 'EMA2': [], 'span1':f'EMA{span1}','span2':f'EMA{span2}'}
    data['ticker'] = ticker
    for row in df.itertuples():
        data['labels'].append(int(str(row.Index.date().year)+str(row.Index.date().month).zfill(2)+str(row.Index.date().day).zfill(2)))
        data['data'].append(row.Volume/pow(10,9))
        data['Adj_close'].append(round(row._5,2))
        data['EMA1'].append(round(row.EMA1,2))
        data['EMA2'].append(round(row.EMA2,2))
    return data



def price_chart(request):
    yf.pdr_override()
    try:
        ticker = request.POST['''price_ticker''']
    except:
        try:
            ticker = request.POST['''ticker''']
        except:
            ticker ='AAPL'
    try:
        days = int(request.POST['''days'''])
    except:
        days = 90
    try:
        sample = int(request.POST['''sample'''])
    except:
        sample = 1
    try:
        span1 = int(request.POST['''span1'''])
    except:
        span1 = 5
    try:
        span2 = int(request.POST['''span2'''])
    except:
        span2 = 15
    print(ticker, days, sample)
    ticker = ticker.upper()
    # print(statements.get_statement(ticker))
    data =get_price_data(ticker, days, sample, span1, span2)
    return render(request, 'analytics/analytics.html', data)
    # return JsonResponse(data)



def analytics_with_pivot_rough(request):
    yf.pdr_override()
    try:
        ticker = request.POST['''ticker''']
    except:
        ticker ='AAPL'
    ticker = ticker.upper()
    data = my_custom_sql(f"select date from analytics_priceinfo where ticker = '{ticker}' order by date desc limit 1")
    data['tables'] = tables
    found = False
    if data['rows'] == []:
        start = dt.datetime.now() - dt.timedelta(days=365*5)
    else:
        found = True
        start = data['rows'][0][0]
    print(start)
    now = dt.datetime.now()
    df = pdr.get_data_yahoo(ticker, start, now)
    model_instances = [PriceInfo(
        date=row.Index.date(),
        high =round(row.High,2) ,
        low = round(row.Low,2),
        open = round(row.Open,2),
        close = round(row.Close,2),
        volume = row.Volume,
        adj_clsoe =round(row._5,2),
        ticker =ticker
    ) for row in df.itertuples()]
    if found:
        my_custom_sql(f"delete from analytics_priceinfo where ticker = '{ticker}' and date >= '{start}'")
    PriceInfo.objects.bulk_create(model_instances)
    return render(request, 'analytics/analytics.html', data)


def pivot_data(request):
    dataset = StockTicker.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

