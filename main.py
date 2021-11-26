# bot.py
import os
import nextcord
from nextcord.ext import commands

from dotenv import load_dotenv
from datetime import datetime
from src.CoinMarketCapAPI import cmc
from src.CryptoChart import chart

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    
@bot.command(name = 'c', description = 'less info')
async def crypto_(ctx, *, arg):
    currency_symbol = '$'

    # making crypto and crypto_chart global so it can be used anywhere
    global crypto
    global big_chart
    global small_chart

    # get crypto information and chart
    crypto = cmc()
    crypto.quote(arg) # object   
    crypto_chart = chart(crypto.id)
    big_chart = crypto_chart.create_chart(crypto.percent_change_30d, day = 30, big_chart = True) # url
    small_chart = crypto_chart.create_chart(crypto.percent_change_24h) # url

    # successfuly received infromation from CoinMarketCap
    if not crypto.error:

        view = ToggleEmbed()      
        msg = await ctx.send(embed = create_embed(more = True, currency_symbol = currency_symbol), view = view)
        view.timeout = 5.0
        # waiting for intereaction
        while True:
            await view.wait() 
            if view.value is None:
                view.read_less(disable = True)
                view.read_more(disable = True)
                break
            elif view.value:
                view = ToggleEmbed()  
                await msg.edit(embed = create_embed(more = True, currency_symbol = currency_symbol), view = view)
            else:
                view = ToggleEmbed()  
                await msg.edit(embed = create_embed(currency_symbol = currency_symbol), view = view)


    # if no information received about crypto
    elif 'couldn\'t find' in crypto.error:
        await ctx.send(crypto.error)

    # if I run into API issues send the error and and let the user contact me    
    else: 
        await ctx.send(f'{crypto.error}. please contact <@!240566530239234049>')


@bot.command(name = "q")
async def testing(ctx):

    await ctx.send(
        "Status: OFF",
        components = [
            Button(label = "power switch", style = 3, custom_id = "button1")
        ])

    while True:
        try:
            interaction = await bot.wait_for("button_click", check = lambda i: i.custom_id == "button1", timeout = 5)

            #if interaction.bu
            await interaction.message.edit(
                content = "Status: ON", 
                components = [
                    Button(label = "power switch", style = 4, custom_id = "button1")
                ])
            
           
            await interaction.message.edit(
                "Status: OFF",
                components = [
                    Button(label = "power switch", style = 3, custom_id = "button1")
                ])
        except:
            await interaction.message.edit('---------')
            await interaction.disable_components()
            break


def create_embed(more: bool = False, currency_symbol: str = '$'):
    '''Creates my embed 

    Parameter
    ---------
    more : `bool`
        a bigger embed with more information on the crypto
    
    currency_symbol : `str`
        currency symbol can be `$`, `£`, `€`
    '''

    # formating the name of the crypto so it works with urlh
    url_name = crypto.name.replace(' ', '-') 
    
    # create an embed with more information
    if more:
        embed = nextcord.Embed(
        title = f'{crypto.name}\u200b \u200b `{crypto.symbol}`',
        description = f'**{currency_symbol}{crypto.price}\u200b \u200b `{crypto.percent_change_24h}%`**\u200b \u200b [🔗](https://coinmarketcap.com/currencies/{url_name})\n\u200b',
        color=0x2f3136,  
        timestamp = datetime.strptime(crypto.last_updated, '%Y-%m-%dT%H:%M:%S.%fZ')) # date and time format

        embed.set_thumbnail(url = crypto.logo)

        # show this if coin/token has a platform
        if crypto.platform:
            embed.add_field(name = f'{crypto.platform_name}\u200b \u200b `{crypto.platform_symbol}`', value = f'`{crypto.token_address}` <:metamask:913158673583472650>', inline = False)
        
        # checks if volume can be devide by market cap
        volume_mrkcap = ''
        if float(crypto.market_cap.replace(',', '')) > 0 and float(crypto.volume_24h.replace(',', '')) > 0:
            volume_mrkcap = round(float(crypto.volume_24h.replace(',', ''))/float(crypto.market_cap.replace(',', '')), 4)
            volume_mrkcap = f'```text\nVolume / Market Cap\n{volume_mrkcap}```'

        # market cap, volume and supply information
        embed.add_field(
            name = '\u200b\n', 
            value = f''' ```text\nMarket Cap\n{currency_symbol}{crypto.market_cap}``` ```text\nFully Diluted Market Cap\n{currency_symbol}{crypto.fully_diluted_market_cap}``` ```text\nVolume 24h\n{currency_symbol}{crypto.volume_24h}``` ```text\nCirculating Supply\n{crypto.circulating_supply} {crypto.symbol}``` ```text\nTotal Supply\n{crypto.total_supply} {crypto.symbol}``` {volume_mrkcap}''')
        

        # chart and additional infromation
        embed.add_field(name = f'\u200b',value = f'**30d chart**', inline = False)
        embed.set_footer(text = f'\u200b\n{crypto.name} is now trading at {currency_symbol}{crypto.price} {crypto.currency}, with a 24-hour trading volume of {currency_symbol}{crypto.volume_24h} {crypto.currency}. Our {crypto.symbol} to {crypto.currency} pricing is updated in real time. {crypto.name}\'s pricing has changed by {crypto.percent_change_30d}% in the last 30 days. {crypto.name} has moved {crypto.percent_change_24h}% in price and {crypto.volume_change_24h}% in volume in the last 24 hours. Since {crypto.date_added[:9]}, live {crypto.name} data has been available on CoinMarketCap and is currently ranked #️{crypto.cmc_rank}.')
        #embed.set_image(url = big_chart)
    
    # embed with little information
    else: 
        embed = nextcord.Embed(
        title=f'{crypto.name} `{crypto.symbol}` `{crypto.percent_change_24h}%`', 
        color=0x2f3136,  
        timestamp = datetime.strptime(crypto.last_updated, '%Y-%m-%dT%H:%M:%S.%fZ'))
        embed.set_author(name=f'{currency_symbol}{crypto.price}', icon_url=crypto.logo)
        embed.set_footer(text = f' 24h chart', icon_url = 'https://i2.wp.com/blog.coinmarketcap.com/wp-content/uploads/2019/06/wp-favicon.png')
        #embed.set_image(url = small_chart)
    return embed
    

class ToggleEmbed(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label = 'read more...', style = nextcord.ButtonStyle.gray)
    async def read_more(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

    @nextcord.ui.button(label = 'read less...', style = nextcord.ButtonStyle.gray)
    async def read_less(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        self.stop()


bot.run(TOKEN)

# 16/11/2021
# fiexed search term not being lowercase
# fixed search term not being seperated with - instead of spaces
# doesn't crash when there is no market cap, volume etc.
# embed sends image if not using discord-component library

# 24/11/2021
# made the embed much more readable
# my images are uploaded to imgur
# buttons now work 
# I need to display one button at a time
# do slash commands