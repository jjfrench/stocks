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
        future = session.get(href, headers={'user-agent': 'scrapper'})
        future.info = href
        futures.append(future)
    return as_completed(futures)

def dataset(data, datajson, TICKER):
    """
        Args:
            data (json object):
            TICKER (json key):
    """
    # with open('data.json', 'w') as output:
    dataset_time = time.time()
    for request in data[TICKER]:
        if 'https://www.investors.com/' in request['href']:
            pass
        else:
            _futures = futures(request['href'], workers=250)
        # print(_futures)
            for future in _futures:
                # print(future.info)
                html = future.result().text
                soup = BeautifulSoup(html,'lxml').find_all('h1')
                _json = bs2json().convertAll(soup)
                request['body'] = _json
    print('--- %s seconds ---' % (time.time() - dataset_time))
    # with open('data.json', 'w') as output:
    json.dump(data, datajson, indent=2)

def finviz(datajson):
    """
        Uses global tickers to scrape finviz for stock data
    """
    _futures = futures('https://www.finviz.com/quote.ashx?t=', extension=TICKERS, workers=10)
    data = {} # data 
    for future in _futures:
        print(future.info)
        html = future.result().text
        soup = BeautifulSoup(html,'lxml').find_all(id='news-table')
        for item in soup:
            soup = item.find_all('a')
            _json = bs2json().convertAll(soup)
            data[future.info] = [] # data storage
            for link in _json:
                # Read from file and check existing data
                # to reduce time
                for item in datajson[future.info]:
                    if link['text'] in item['text']:
                        pass
                    else:
                        data[future.info].append({
                            'text':link['text'],
                            'href':link['attributes']['href']
                        })
    for TICKER in data:
        x = threading.Thread(target=dataset, args=(data, datajson, TICKER))
        x.start()
    
    print(threading.active_count())
    # with open('data.json', 'w') as output:
    json.dump(data, datajson, indent=2)

def main():
    fileopen = open('data.json', 'w+')
    datajson = json.load(fileopen)
    start_time = time.time()
    finviz(datajson)
    print('--- %s seconds ---' % (time.time() - start_time))

if __name__ == '__main__':
    main()