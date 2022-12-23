# TODO: implement tests, blacktea like game, images

import discord
from discord.ext import commands
import random
import config
import json
from PIL import Image, ImageDraw, ImageFont
import os
from os.path import exists
import string

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix = '-', description = description, intents = intents, activity = discord.Activity(type = discord.ActivityType.watching, name = "-help"))

@bot.event
async def on_ready():
    await bot.load_extension('jishaku')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

hiraganaData = []
with open("hiragana.json", encoding = "utf8") as hiraganaJSON:
    hiraganaJSON = json.loads(hiraganaJSON.read())
for i in hiraganaJSON:
    hiraganaData.append([i["kana"], i["romaji"]])

basicHiragana = []

katakanaData = []
with open("katakana.json", encoding = "utf8") as katakanaJSON:
    katakanaJSON = json.loads(katakanaJSON.read())
for i in katakanaJSON:
    katakanaData.append([i["kana"], i["romaji"]])

darkMode = False

@bot.command()
async def darkmode(ctx):
    global darkMode
    embed = discord.Embed()
    
    if darkMode:
        embed.color = 0xFFFFFF
        embed.title = "Dark Mode Turned Off"
        embed.set_footer(text = f"Light Mode requested by {ctx.author.display_name}", icon_url = ctx.author.avatar.url)
    else:
        embed.color = 0x000000
        embed.title = "Dark Mode Turned On"
        embed.set_footer(text = f"Dark Mode requested by {ctx.author.display_name}", icon_url = ctx.author.avatar.url)

    darkMode = not darkMode

    await ctx.send(embed = embed)
    

async def kana(ctx, type: str):
    if type != "hiragana" and type != "katakana":
        return

    check = None
    randKana = None
    if type == "hiragana":
        randKana = hiraganaData[random.randint(0, len(hiraganaData))]
        check = "Hiragana"
    elif type == "katakana":
        randKana = katakanaData[random.randint(0, len(katakanaData))]
        check = "Katakana"

    ttf = ImageFont.truetype("ARIALUNI.TTF", 256)
    message = str(randKana[0])
    width = 512
    height = 512

    img = Image.new("RGB", (width, height), color = "black" if darkMode else "white")
    imgDraw = ImageDraw.Draw(img)
    textWidth, textHeight = imgDraw.textsize(message, font = ttf)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2

    imgDraw.text((xText, yText), message, fill = "white" if darkMode else "black", font = ttf)

    digits = 24
    def generateCrypt(d: int):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k = d))
        
    fileName = generateCrypt(digits)
    while exists(f"{fileName}.png"):
        fileName = generateCrypt(digits)

    img.save(f"{fileName}.png")

    embed = discord.Embed()
    embed.title = f"**{check}**"
    embed.add_field(name = "Character", value = f"**{randKana[0]}**", inline = True)
    embed.add_field(name = "Romaji", value = f"||{randKana[1]}||", inline = True)
    embed.color = 0x61D67E
    embed.set_footer(text = f"{check} requested by {ctx.author.display_name}", icon_url = ctx.author.avatar.url)

    file = discord.File(f"{fileName}.png", filename = f"{fileName}.png")
    embed.set_image(url = f"attachment://{fileName}.png")

    await ctx.send(file = file, embed = embed)

    os.remove(f"{fileName}.png")


@bot.command(aliases=["h"])
async def hiragana(ctx):
    await kana(ctx, "hiragana")

@bot.command(aliases=["k"])
async def katakana(ctx):
    await kana(ctx, "katakana")

bot.run(config.token)

