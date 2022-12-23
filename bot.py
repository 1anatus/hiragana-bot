# This example requires the 'members' and 'message_content' privileged intents to function.
# TODO: implement tests, blacktea like game, images

import discord
from discord.ext import commands
import random
import config
import json
from PIL import Image, ImageDraw, ImageFont
description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix = '-', description = description, intents = intents)

@bot.event
async def on_ready():
    await bot.load_extension('jishaku')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


with open("hiragana.json", encoding = "utf8") as hiraganaJSON:
    hiraganaJSON = json.loads(hiraganaJSON.read())

hiraganaData = []
for i in hiraganaJSON:
    hiraganaData.append([i["kana"], i["romaji"]])

basicHiragana = []

@bot.command()
async def hiragana(ctx):
    randHiragana = hiraganaData[random.randint(0, len(hiraganaData))]
    ttf = ImageFont.truetype("ARIALUNI.TTF", 256)
    message = str(randHiragana[0])
    width = 512
    height = 512

    img = Image.new("RGB", (width, height), color = "white")
    imgDraw = ImageDraw.Draw(img)
    textWidth, textHeight = imgDraw.textsize(message, font = ttf)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2

    imgDraw.text((xText, yText), message, fill = "black", font = ttf)

    img.save("hiragana.png")

    embed = discord.Embed()
    embed.title = "**Hiragana**"
    embed.add_field(name = "Character", value=f"**{randHiragana[0]}**", inline = True)
    embed.add_field(name = "Romaji", value=f"||{randHiragana[1]}||", inline = True)
    embed.color = 0x61D67E
    embed.set_footer(text = f"Hiragana requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

    file = discord.File("hiragana.png", filename = "hiragana.png")
    embed.set_image(url = "attachment://hiragana.png")

    await ctx.send(file = file, embed = embed)

bot.run(config.token)

