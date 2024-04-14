from core.core import VocalizeCore
from dotenv import load_dotenv
import asyncio

load_dotenv()

bot = VocalizeCore()

async def main():
    await bot.run()


asyncio.run(main())
