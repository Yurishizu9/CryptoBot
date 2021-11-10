'''
gets crypto quotes form caoinmarketcap
'''
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooMany
import json
import os

class Quotete:
    
    def __init__nit__(self, search_term):
        self.search_term = search_term

        
KEY = os.environ['COINMARKETCAP_API']
quote_latest = '/1/currency/quotes/latest'
url = 'https://pro-api.coinmarketcap.com' + quote_latest

parameters = {
  'slug': 'bitcoin',
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': KEY,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  pprint.pprint(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  pprint.pprint(e)

# get the name of the key
crypto_id = None
for x in data['data'].keys(): crypto_id = x

# essential data
circulating_supply = data['data'][crypto_id]['circulating_supply']
cmc_rank = data['data'][crypto_id]['cmc_rank']
date_added = data['data'][crypto_id]['date_added']
last_updated = data['data'][crypto_id]['last_updated']
max_supply = data['data'][crypto_id]['max_supply']
name = data['data'][crypto_id]['name']
symbol = data['data'][crypto_id]['symbol']
total_supply = data['data'][crypto_id]['total_supply']
fully_diluted_market_cap = data['data'][crypto_id]['quote']['USD']['fully_diluted_market_cap']
market_cap = data['data'][crypto_id]['quote']['USD']['market_cap']
logo = f'https://s2.coinmarketcap.com/static/img/coins/64x64/{crypto_id}.png'

# USD, currency may change
if data['data'][crypto_id]['quote'] == 'USD':
    percent_change_1h = data['data'][crypto_id]['quote']['USD']['percent_change_1h']
    percent_change_24h = data['data'][crypto_id]['quote']['USD']['percent_change_24h']
    percent_change_30d = data['data'][crypto_id]['quote']['USD']['percent_change_30d']
    price = data['data'][crypto_id]['quote']['USD']['price']
    volume_24h = data['data'][crypto_id]['quote']['USD']['volume_24h']
    volume_change_24h = data['data'][crypto_id]['quote']['USD']['volume_change_24h']

# platform, not all coin have platforms
if data['data'][crypto_id]['platform'] != None:
    platform_name = data['data'][crypto_id]['platform']['name']
    platform_symbol = data['data'][crypto_id]['platform']['symbol']
    token_address = data['data'][crypto_id]['platform']['token_address']

