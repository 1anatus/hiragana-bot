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

bot = commands.Bot(owner_ids=[681208628350418977, 468101575689109525], command_prefix = '-', description = description, intents = intents, activity = discord.Activity(type = discord.ActivityType.watching, name = "-help"))

@bot.event
async def on_ready():
    await bot.load_extension("jishaku")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

def kanaToList(type: str, basic: bool = False):
    kanaData = []
    with open(f"{type}.json", encoding = "utf8") as kanaJSON:
        kanaJSON = json.loads(kanaJSON.read())

    for i in kanaJSON:
        if basic:
            if len(i["kana"]) == 1:
                kanaData.append([i["kana"], i["romaji"]])
        else:
            kanaData.append([i["kana"], i["romaji"]])    

    return kanaData

hiraganaData = kanaToList("hiragana")
basicHiraganaData = kanaToList("hiragana", True)

katakanaData = kanaToList("katakana")
basicKatakanaData = kanaToList("katakana", True)


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
    

async def kana(ctx, type: str, basic: bool = False):
    kanaScripts = ["hiragana", "katakana"]
    if not type in kanaScripts:
        ctx.send("nah")
        return

    check = None
    randKana = None
    if type == "hiragana":
        if basic:
            randKana = basicHiraganaData[random.randint(0, len(basicHiraganaData))]
        else:
            randKana = hiraganaData[random.randint(0, len(hiraganaData))]

        check = ["ひらがな", "Hiragana"]
    elif type == "katakana":
        if basic:
            randKana = basicKatakanaData[random.randint(0, len(basicKatakanaData))]
        else:
            randKana = katakanaData[random.randint(0, len(katakanaData))]

        check = ["カタカナ", "Katakana"]

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
    embed.title = f"**{check[0]} | {check[1]}**"
    embed.add_field(name = "Character" if len(randKana[0]) == 1 else "Digraph", value = f"**{randKana[0]}**", inline = True)
    embed.add_field(name = "Rōmaji", value = f"||{randKana[1]}||", inline = True)
    embed.color = 0x61D67E
    embed.set_footer(text = f"{check[0]} requested by {ctx.author.display_name}", icon_url = ctx.author.avatar.url)

    file = discord.File(f"{fileName}.png", filename = f"{fileName}.png")
    embed.set_image(url = f"attachment://{fileName}.png")

    await ctx.send(file = file, embed = embed)

    os.remove(f"{fileName}.png")


@bot.command(aliases = ["h"])
async def hiragana(ctx):
    await kana(ctx, "hiragana")

@bot.command(aliases = ["bh"])
async def basichiragana(ctx):
    await kana(ctx, "hiragana", True)

@bot.command(aliases = ["k"])
async def katakana(ctx):
    await kana(ctx, "katakana")

@bot.command(aliases = ["bk"])
async def basickatakana(ctx):
    await kana(ctx, "katakana", True)

bot.run(config.token)

