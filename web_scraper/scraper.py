
from requests import get
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from bs4 import BeautifulSoup
from bs2json import bs2json
import time
import json

def main():
    start_time = time.time()
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))
    TICKERS = [
        'BEEM',
        'AMD',
        'REGI',
        'LOGI'
    ]

    futures = [
        session.get(f'https://www.finviz.com/quote.ashx?t={TICKER}', headers={'user-agent': 'scrapper'}) 
            for TICKER in TICKERS
        ]

    for index, future in enumerate(as_completed(futures)):
        html = future.result().text
        soup = BeautifulSoup(html,'lxml').find_all(id='news-table')
        _json = bs2json().convertAll(soup)
        with open('data.txt', 'w') as output:
            json.dump(_json[index], output, indent=2)
        break
        

    print("--- %s seconds ---" % (time.time() - start_time))
    

if __name__ == "__main__":
    main()