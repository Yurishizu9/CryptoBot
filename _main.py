# bot.py
import os
import discord
from discord.ext import commands

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

    
@bot.command(name='c', description = 'less info')
async def crypto_(ctx, *, arg):
    currency_symbol = '$'
    more_info = True

    # making crypto and crypto_chart global so it can be used anywhere
    global crypto
    global crypto_chart

    # get crypto information
    crypto = cmc()
    crypto.quote(arg)
    
    # successfuly received infromation from CoinMarketCap
    if not crypto.error:

        # get svg chart
        crypto_chart = chart(crypto.id)
        
        # create a bigger chart
        if more_info:
            crypto_chart.create_chart(crypto.percent_change_30d, day = 30, big_chart = True)
        else: # create a small chart
            crypto_chart.create_chart(crypto.percent_change_24h)

        # send embed
        # Discord.file allows me to send locally saved image with an embed
        chart_png = discord.File(crypto_chart.path, filename = crypto_chart.name)      
        await ctx.send(file = chart_png, embed = create_embed(more = more_info, currency_symbol = currency_symbol))
    
    # if no information received about crypto
    elif 'couldn\'t find' in crypto.error:
        await ctx.send(crypto.error)

    # if I run into API issues send the error and and let the user contact me    
    else: 
        await ctx.send(f'{crypto.error}. please contact <@!240566530239234049>')


@bot.command(  name='test2', description = 'more info')
async def crypto_(ctx):
    # embed = discord.Embed(
    #     title='Bitcoin `BTC`', 
    #     description='**$6602.60** `-0.15%` ```text\n Rank #1```\u200b',
    #     color=0x2f3136,  
    #     timestamp = datetime.utcnow())
    # #   timestamp = datetime.strptime('2013-04-28T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')

    # embed.set_thumbnail(url='https://s2.coinmarketcap.com/static/img/coins/64x64/1.png')
    # embed.add_field(name='$852,164,659,250', value='**`↳ Market Cap`**', inline = False)
    # embed.add_field(name='$952,835,089,431', value='**`↳ Fully Diluted Market Cap`**', inline = False)
    # embed.add_field(name='$4,314,444,687', value='**`↳ Volume 24h`**', inline = False)
    # embed.add_field(name='0.03158', value='**`↳ Volume / Market Cap`**', inline = False)
    # embed.add_field(name='17,199,862 BTC', value='**`↳ Circulating Supply`**', inline = False)
    # embed.add_field(name='17,199,862 BTC', value='**`↳ Total Supply`**', inline = False)
    # embed.add_field(name='21,000,000 BTC', value='**`↳ Max Supply`**', inline = False)
    # embed.set_footer(text = f'CoinMarketCap', icon_url = 'https://i2.wp.com/blog.coinmarketcap.com/wp-content/uploads/2019/06/wp-favicon.png')

    # locally saved png will be attached to discord embed
    embed = discord.Embed(title="Title", description="Desc", color=0x00ff00) #creates embed
    file = discord.File("svgs/image.png", filename="image.png")
    embed.set_image(url="attachment://image.png")
    await ctx.send(file = file, embed=embed)



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

def create_embed(more: bool, currency_symbol: str):
    '''Creates my embed 

    Parameter
    ---------
    more : `bool`
        a bigger embed with more information on the crypto
    
    currency_symbol : `str`
        currency symbol can be `$`, `£`, `€`
    '''
    
    # create an embed with more information
    if more:
        embed = discord.Embed(
        title = f'{crypto.name} `{crypto.symbol}`', 
        description = f'**{currency_symbol}{crypto.price}** `{crypto.percent_change_24h}%` ```text\n Rank #{crypto.cmc_rank}```\u200b',
        color=0x2f3136,  
        timestamp = datetime.strptime(crypto.last_updated, '%Y-%m-%dT%H:%M:%S.%fZ')) # date and time format

        embed.set_thumbnail(url = crypto.logo)

        # show this if coin/token has a platform
        if crypto.platform:
            embed.add_field(name = f'Token on {crypto.platform_name} `{crypto.platform_symbol}`', value = f'**`{crypto.token_address}`**', inline = False)
        
        embed.add_field(name = f'{currency_symbol}{crypto.market_cap}', value = '**`↳ Market Cap`**', inline = False)
        embed.add_field(name = f'{currency_symbol}{crypto.fully_diluted_market_cap}', value = '**`↳ Fully Diluted Market Cap`**', inline = False)
        embed.add_field(name = f'{currency_symbol}{crypto.volume_24h}', value = '**`↳ Volume 24h`**', inline = False)
        
        # ignore if market cap or 24h volume is 0 
        if float(crypto.market_cap.replace(',', '')) > 0 and float(crypto.volume_24h.replace(',', '')) > 0:
            embed.add_field(name = round(float(crypto.volume_24h.replace(',', ''))/float(crypto.market_cap.replace(',', '')), 4), value='**`↳ Volume / Market Cap`**', inline = False)
        
        embed.add_field(name = f'{crypto.circulating_supply} {crypto.symbol}', value = '**`↳ Circulating Supply`**', inline = False)
        embed.add_field(name = f'{crypto.total_supply} {crypto.symbol}', value = '**`↳ Total Supply`**', inline = False)
                
        # summary
        embed.add_field(
            name = f'__{crypto.name} Price Live Data__',
            value = f'**{crypto.name}** is now trading at **{currency_symbol}{crypto.price} {crypto.currency}**, with a 24-hour trading volume of **{currency_symbol}{crypto.volume_24h} {crypto.currency}**. Our **{crypto.symbol}** to **{crypto.currency}** pricing is updated in real time. **{crypto.name}\'s** pricing has changed by **{crypto.percent_change_30d}%** in the last 30 days. **{crypto.name}** has moved **{crypto.percent_change_24h}%** in price and **{crypto.volume_change_24h}%** in volume in the last 24 hours. Since **{crypto.date_added[:9]}**, live **{crypto.name}** data has been available on CoinMarketCap and is currently  ranked **#{crypto.cmc_rank}.**\n\n__**{crypto.name} to {crypto.currency}**__ `{crypto_chart.day}d chart`', inline = True)
        
        embed.set_footer(text = f'Data provided by CoinMarketCap', icon_url = 'https://i2.wp.com/blog.coinmarketcap.com/wp-content/uploads/2019/06/wp-favicon.png')
        embed.set_image(url = f'attachment://{crypto_chart.name}')
    
    # embed with little information
    else: 
        embed = discord.Embed(
        title=f'{crypto.name} `{crypto.symbol}` `{crypto.percent_change_24h}%`', 
        color=0x2f3136,  
        timestamp = datetime.strptime(crypto.last_updated, '%Y-%m-%dT%H:%M:%S.%fZ'))
        embed.set_author(name=f'{currency_symbol}{crypto.price}', icon_url=crypto.logo)
        embed.set_footer(text = f' 24h chart', icon_url = 'https://i2.wp.com/blog.coinmarketcap.com/wp-content/uploads/2019/06/wp-favicon.png')
        embed.set_image(url = f'attachment://{crypto_chart.name}')
    return embed
    

bot.run(TOKEN)

# fiexed search term not being lowercase
# fixed search term not being seperated with - instead of spaces
# doesn't crash when there is no market cap, volume etc.
# embed sends image if not using discord-component library
