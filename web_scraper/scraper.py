
from requests import get
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from bs4 import BeautifulSoup
from bs2json import bs2json
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
    start_time = time.time()
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))
    
    futures = [
        session.get(f'https://www.finviz.com/quote.ashx?t={TICKER}', headers={'user-agent': 'scrapper'}) 
            for TICKER in TICKERS
        ]

    data = []
    for future in as_completed(futures):
        html = future.result().text
        soup = BeautifulSoup(html,'lxml').find_all(id='news-table')
        for item in soup:
            soup = item.find_all('a')
            _json = bs2json().convertAll(soup)
            data.append(_json)
    with open('data.txt', 'w') as output:
        json.dump(data, output, indent=2)

    print("--- %s seconds ---" % (time.time() - start_time))

def main():
    finviz()

if __name__ == "__main__":
    main()