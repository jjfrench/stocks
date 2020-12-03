# ____________Imports____________
from requests import get
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from bs2json import bs2json
from analyze import *
import threading
import time
import json


TICKERS = [
    'BEEM',
    'AMD',
    'REGI',
    'LOGI',
    'TSLA'
]

def futures(href, extension=None, workers=10):
    """
        Args:
            href (array of strings): href(s)
            extension (string):
            workers (int):
    """
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=workers))
    futures = []
    # Single Link with multiple extensions
    if extension:
        for item in extension:
            future = session.get(href+item, headers={'user-agent': 'scrapper'})
            future.info = item
            futures.append(future)
    # Multiple Links no extensions
    else:
        for link in href:
            future = session.get(link, headers={'user-agent': 'scrapper'})
            future.info = None
            futures.append(future)
    return as_completed(futures)

def dataset(data, TICKER):
    for request in data[TICKER]:
            _futures = futures(request['href'], workers=25)
            request['Complete'] = 'done'

def finviz():
    """
        Uses global tickers to scrape finviz for stock data
    """
    _futures = futures('https://www.finviz.com/quote.ashx?t=', extension=TICKERS, workers=10)

    data = {} # data storage
    for future in _futures:
        print(future.info)
        html = future.result().text
        soup = BeautifulSoup(html,'lxml').find_all(id='news-table')
        for item in soup:
            soup = item.find_all('a')
            _json = bs2json().convertAll(soup)
            data[future.info] = [] # data storage
            for link in _json:
                data[future.info].append({
                    'text':link['text'],
                    'href':link['attributes']['href']
                })
    for TICKER in data:
        dataset(data, TICKER)

    with open('data.json', 'w') as output:
        json.dump(data, output, indent=2)
    # with open('data.txt', 'w') as output:
    #     json.dump(_json, output, indent=2)

def main():
    start_time = time.time()
    finviz()
    print('--- %s seconds ---' % (time.time() - start_time))

if __name__ == '__main__':
    main()