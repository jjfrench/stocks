from requests import get
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from bs4 import BeautifulSoup
import time
import json

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

for future in as_completed(futures):
    html = future.result().text
    # pprint({
    #     'url': resp.request.url,
    #     'content': resp.text,
    # })
    soup = BeautifulSoup(html,'lxml')
    soup = soup.find_all(id='news-table')
    print(soup)

print("--- %s seconds ---" % (time.time() - start_time))