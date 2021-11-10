class Chart:
    '''
    downloads and modifies svg chart from CoinMarketCap
    
    ---
    Attributes
    ----------
    id : `int`
        ID of the crypto from CoinMarketCap API
        
    period : `int`, optional
        time period of chart in days (`default is 1`) supports `1`, `7`, `30`, `90` day(s)
    

    Methods
    -------
    save_chart(percent_change) -> `str` png_path
        will get svg chart, changeline colour based on `percent_change` and save as png  
    '''  

    def __init__(self, crypto_id:int, period:int = 1):
        ''' 
        Parameters
        ----------
        id : `int`
            ID of the crypto from CoinMarketCap API
            
        period : `int`, optional
            time period of chart in days (`default = 1`) supports `1`, `7`, `30` day(s)
        '''
        self.id = crypto_id
        self.period = period

    
    def save_chart(self, percent_change: float):
        '''will get svg chart, change line colour based on `percent_change` and save as png
        
        ---
        Parameters
        ----------
        percent_change : `float`
            percentage change of the crypto will use this value to determine if chart is +green  or -red.
            Supports `percent_change_24h`, `percent_change_7d`, `percent_change_30d` from CoinMarketCap API 
            https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesLatest
        
        
        Returns
        -------
        png_path : `str`
            the file location of the png chart
        '''
        self.png_path = ''

import requests
from svglib.svglib import svg2rlg
import io
from reportlab.graphics import renderPDF, renderPM


# get SVG chart content
day = 7
crypto_id = 1
r = requests.get(f'https://s3.coinmarketcap.com/generated/sparklines/web/{day}d/2781/{crypto_id}.svg')

# replace the colour of the lines in the chart
svg_chart = r.text
red = 'stroke:rgb(234,57,67)'
green = 'stroke:rgb(22,199,132)'
svg_chart = svg_chart.replace('stroke:rgb(237,194,64)', red)

# make background match embed and remove unwanted lines of code
svg_chart = svg_chart.replace('style="fill:rgb(255,255,255);fill-opacity:0', 'style="fill: rgb(47,49,54);fill-opacity: 100')
svg_chart = svg_chart.replace('<?xml version="1.0" encoding="UTF-8" standalone="no"?>', '')

# save svg as png
svg_io = io.StringIO(svg_chart)
drawing = svg2rlg(svg_io)
scale = 10
drawing.scale(scale, scale)
drawing.width *= scale
drawing.height *= scale
renderPM.drawToFile(drawing, f"svgs/{day}D-{crypto_id}.png", fmt="PNG")
