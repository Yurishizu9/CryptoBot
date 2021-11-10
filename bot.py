import os
import random

import discord
from discord.ext import commands
from datetime import datetime
#from dotenv import load_dotenv
#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')


TOKEN = os.environ['DISCORD_TOKEN']
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(  name='c', description = "less info")
async def crypto_(ctx):
    embed = discord.Embed(
        title="Bitcoin `BTC` `-0.15% `", 
        color=0x2f3136,  
        timestamp = datetime.utcnow())
    #   timestamp = datetime.strptime("2013-04-28T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    embed.set_author(name="$6602.60", icon_url='https://s2.coinmarketcap.com/static/img/coins/64x64/1.png')
    embed.set_image(url = "https://s3.coinmarketcap.com/generated/sparklines/web/1d/2781/1.png")
    embed.set_footer(text = f"CoinMarketCap", icon_url = "https://i2.wp.com/blog.coinmarketcap.com/wp-content/uploads/2019/06/wp-favicon.png")
    await ctx.send(embed=embed)


@bot.command(  name='cc', description = "more info")
async def crypto_(ctx):
    embed = discord.Embed(
        title="Bitcoin `BTC`", 
        description="**$6602.60** `-0.15%` ```text\n Rank #1```\u200b",
        color=0x2f3136,  
        timestamp = datetime.utcnow())
    #   timestamp = datetime.strptime("2013-04-28T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")

    embed.set_thumbnail(url="https://s2.coinmarketcap.com/static/img/coins/64x64/1.png")
    embed.add_field(name="$852,164,659,250", value="**`↳ Market Cap`**", inline = False)
    embed.add_field(name="$952,835,089,431", value="**`↳ Fully Diluted Market Cap`**", inline = False)
    embed.add_field(name="$4,314,444,687", value="**`↳ Volume 24h`**", inline = False)
    embed.add_field(name="0.03158", value="**`↳ Volume / Market Cap`**", inline = False)
    embed.add_field(name="17,199,862 BTC", value="**`↳ Circulating Supply`**", inline = False)
    embed.add_field(name="17,199,862 BTC", value="**`↳ Total Supply`**", inline = False)
    embed.add_field(name="21,000,000 BTC", value="**`↳ Max Supply`**", inline = False)
    embed.set_footer(text = f"CoinMarketCap", icon_url = "https://i2.wp.com/blog.coinmarketcap.com/wp-content/uploads/2019/06/wp-favicon.png")

    png_chart = discord.File("file.png", filename="file.png")
    embed.set_image(url="attachment://file.png")
    await ctx.send(file=png_chart, embed=embed)

@bot.command()
async def q(ctx):
    f = discord.File("./file.png", filename="file.png")
    e = discord.Embed(title = "this image", description = "is a graph")
    e.set_image(url="attachment://file.png")
    await ctx.send(file=f, embed=e, content = "adhbiasuhbdiusahbid")

bot.run(TOKEN)