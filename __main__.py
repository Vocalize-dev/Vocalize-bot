from core.core import VocalizeCore
import discord
from dotenv import load_dotenv
import asyncio
import os
from logging import DEBUG

load_dotenv()

bot = VocalizeCore(token=os.getenv('BOT_TOKEN'), intents=discord.Intents.all())

discord.utils.setup_logging()

async def main():
    await bot.run()


asyncio.run(main())
