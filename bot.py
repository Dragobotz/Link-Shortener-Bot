# ยฉDragobotz

import re
import aiohttp

from os import environ
from pyrogram import Client, filters
from pyrogram.types import *

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY')
API_URL = environ.get('API_URL')

dragobots = Client('link shortener bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=100)

print("Developer: @DragoBots , Join & Share Channel")
print("Bot is Started Now")

@dragobots.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm Link Shortener bot. Just send me link and get short link, You can also send multiple links seperated by a space or enter.\n\n**Developer:** @DragoBots")


@dragobots.on_message(filters.private & filters.text & filters.incoming)
async def link_handler(bot, message):
    link_pattern = re.compile('https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}', re.DOTALL)
    links = re.findall(link_pattern, message.text)
    if len(links) <1:
        await message.reply("No links Found in this text",quote=True)
        return
    for link in links:
        try:
            short_link = await get_shortlink(link)
            await message.reply(f"๐๐๐ซ๐ ๐ข๐ฌ ๐๐จ๐ฎ๐ซ ๐๐ก๐จ๐ซ๐ญ๐๐ง๐๐ ๐๐ข๐ง๐ค\n\n๐๐ซ๐ข๐ ๐ข๐ง๐๐ฅ ๐๐ข๐ง๐ค: {link}\n\n๐๐ก๐จ๐ซ๐ญ๐๐ง๐๐ ๐๐ข๐ง๐ค: `{short_link}`",quote=True,disable_web_page_preview=True)
        except Exception as e:
            await message.reply(f'๐๐ซ๐ซ๐จ๐ซ: `{e}`', quote=True)


async def get_shortlink(link):
    url = API_URL
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]


dragobots.run()
