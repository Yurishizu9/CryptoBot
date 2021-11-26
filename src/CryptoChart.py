import requests
from svglib.svglib import svg2rlg
import io
from reportlab.graphics import renderPDF, renderPM
from dotenv import load_dotenv
import os
import pyimgur

load_dotenv()
CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')
CLIENT_SECRET = os.getenv('IMGUR_CLIENT_SECRET')



class chart:
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

    def __init__(self, crypto_id : int):
        ''' 
        Parameters
        ----------
        id : `int`
            ID of the crypto from CoinMarketCap API
        '''

        self.id = crypto_id

    
    def create_chart(self, percent_change : float, day : int = 1, big_chart : bool = False):
        '''creates the chart for the and update the `self.path`
        
        ---
        Parameters
        ----------
        percent_change : `float`
            determines if line chart is green (possitive) or red (negative).
            Supports `percent_change_24h`, `percent_change_7d`, `percent_change_30d` from CoinMarketCap API 
            https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesLatest
        
        day : `int`, optional
            time period of chart in days (`default = 1`) supports `1`, `7`, `30` day(s)

        big_chart : `bool`, optional
            if true will scale the chart by `x10` (`default = False`)
        '''

        # get SVG chart content
        r = requests.get(f'https://s3.coinmarketcap.com/generated/sparklines/web/{day}d/2781/{self.id}.svg')

        # replace the colour of the lines in the chart
        svg_chart = r.text
        red = 'stroke:rgb(234,57,67)'
        green = 'stroke:rgb(22,199,132)'
        
        svg_chart = svg_chart.replace('stroke:rgb(237,194,64)', green) if percent_change > 0 else svg_chart.replace('stroke:rgb(237,194,64)', red)

        # make background match embed and remove unwanted lines of code
        svg_chart = svg_chart.replace('style="fill:rgb(255,255,255);fill-opacity:0', 'style="fill: rgb(47,49,54);fill-opacity: 100')
        svg_chart = svg_chart.replace('<?xml version="1.0" encoding="UTF-8" standalone="no"?>', '')

        # save svg as png
        svg_io = io.StringIO(svg_chart)
        drawing = svg2rlg(svg_io)
        
        # scale
        scale = 10 if big_chart else 1
        drawing.scale(scale, scale)
        drawing.width *= scale
        drawing.height *= scale

        # set attributes and render image
        self.day = day
        self.percent = percent_change
        self.name = f'{day}D-{self.id}.png'
        self.path = f'src/{self.name}' #f'svgs/{self.name}'
        renderPM.drawToFile(drawing, self.path, fmt='PNG')

        # uploading image to imgur
        im = pyimgur.Imgur(CLIENT_ID)
        try:
            print('3\n\n\n')
            upload_image = im.upload_image(path = self.path)
            print(upload_image, '\nhey\n\n')
            self.url = upload_image.link
            return self.url
            # cant seem to capture this error
            # Imgur ERROR message: {'code': 429, 'message': 'You are uploading too fast. Please wait 2 more minutes.', 'type': 'ImgurException', 'exception': []}
            # ---------------------------------------------------------------------------------------------------------------------------------------------------
        except:
            print('4\n\n\n\n\n\n\n')
            print(type(upload_image))
            print('5\n\n\n\n\n\n\n')
            print(upload_image.replies)
            print(upload_image.content)
            return None
        




