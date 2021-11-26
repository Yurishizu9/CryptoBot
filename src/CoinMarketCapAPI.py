from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from dotenv import load_dotenv
import pprint
import locale

class cmc:

    def quote(self, search_term, currency = 'USD'):
        ''' gets crypto quotes form caoinmarketcap '''
        
        self.currency = currency
        self.error = None

        # get rid of spaces and make everything lower case
        search_term = search_term.replace(' ', '-').lower()
        #print(search_term)
       
        # make API request
        load_dotenv()
        KEY = os.getenv('COINMARKETCAP_KEY')
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        
        parameters = {
        'slug': search_term,
        'convert': self.currency
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
            #pprint.pprint(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            #pprint.pprint(e)
            pass

        # if no errors continue running
        self.error = data['status']['error_message']
        if self.error == None:
            # get crypto id
            for x in data['data'].keys(): self.id = x

            # essential data
            # locale allows me to format the decimal by seperating them with commas
            # round() allows me to round floats to 2 decimal places
            locale.setlocale(locale.LC_ALL, 'en_us')
            self.circulating_supply = locale.format('%.2f', data['data'][self.id]['circulating_supply'], grouping=True)
            self.cmc_rank = data['data'][self.id]['cmc_rank']
            self.date_added = data['data'][self.id]['date_added']
            self.last_updated = data['data'][self.id]['last_updated']
            self.max_supply = data['data'][self.id]['max_supply'] if data['data'][self.id]['max_supply'] == None else locale.format('%.2f', data['data'][self.id]['max_supply'], grouping=True)
            self.name = data['data'][self.id]['name']
            self.symbol = data['data'][self.id]['symbol']
            self.total_supply = locale.format('%.2f', data['data'][self.id]['total_supply'], grouping=True)
            self.logo = f'https://s2.coinmarketcap.com/static/img/coins/64x64/{self.id}.png'
            self.fully_diluted_market_cap = locale.format('%.2f', data['data'][self.id]['quote'][currency]['fully_diluted_market_cap'], grouping=True)
            self.market_cap = locale.format('%.2f', data['data'][self.id]['quote'][currency]['market_cap'], grouping=True)
            self.percent_change_1h = round(data['data'][self.id]['quote'][currency]['percent_change_1h'], 2)
            self.percent_change_24h = round(data['data'][self.id]['quote'][currency]['percent_change_24h'], 2)
            self.percent_change_30d = round(data['data'][self.id]['quote'][currency]['percent_change_30d'], 2)
            self.price = locale.format('%.2f', data['data'][self.id]['quote'][currency]['price'], grouping=True)
            self.volume_24h = locale.format('%.2f', data['data'][self.id]['quote'][currency]['volume_24h'], grouping=True)
            self.volume_change_24h = round(data['data'][self.id]['quote'][currency]['volume_change_24h'], 2)

            # platform, not all coin have platforms
            self.platform = False
            if data['data'][self.id]['platform'] != None:
                self.platform_name = data['data'][self.id]['platform']['name']
                self.platform_symbol = data['data'][self.id]['platform']['symbol']
                self.token_address = data['data'][self.id]['platform']['token_address']
                self.platform = True

        elif data['status']['error_code'] == 400:
            self.error = f'couldn\'t find "{search_term}"'