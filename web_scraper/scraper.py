from requests import get
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from bs2json import bs2json
from analyze import *
import time
import json


TICKERS = [
    'BEEM',
    'AMD',
    'REGI',
    'LOGI',
    'TSLA'
]

def finviz():
    """
        Uses global tickers to scrape finviz for stock data
    """
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))
    
    futures = []
    for TICKER in TICKERS:
        future = session.get(f'https://www.finviz.com/quote.ashx?t={TICKER}', headers={'user-agent': 'scrapper'})
        future.tick = TICKER
        futures.append(future)

    data = {}
    for future in as_completed(futures):
        print(future.tick)
        html = future.result().text
        soup = BeautifulSoup(html,'lxml').find_all(id='news-table')
        for item in soup:
            soup = item.find_all('a')
            _json = bs2json().convertAll(soup)

            data[future.tick] = []
            for link in _json:
                data[future.tick].append({
                    'text':link['text'],
                    'href':link['attributes']['href']
                })

    with open('data.json', 'w') as output:
        json.dump(data, output, indent=2)
    with open('data.txt', 'w') as output:
        json.dump(_json, output, indent=2)

def main():
    start_time = time.time()
    finviz()
    print('--- %s seconds ---' % (time.time() - start_time))

if __name__ == '__main__':
    main()