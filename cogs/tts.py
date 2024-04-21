from discord.ext import commands
from discord import app_commands, Interaction
from core.core import VocalizeCore
import json
import asyncio


class TextToSpeach(commands.GroupCog, name='tts'):
    def __init__(self, bot: VocalizeCore) -> None:
        self.bot = bot
        super().__init__()


    @app_commands.command()
    async def connect(self, inter: Interaction):
        member = inter.guild.get_member(inter.user.id)
        guild_id = member.guild.id
        channel_id = member.voice.channel.id
        await inter.response.defer()
        def message_check(payload):
            data = json.loads(payload)
            return data["t"] == "VOICE_SERVER_UPDATE" and data["d"]["guild_id"] == str(
                guild_id
            )

        event = asyncio.create_task(
            self.bot.wait_for(
                "socket_raw_receive",
                check=message_check,
            )
        )
        await self.bot.ws.send_as_json(
            {
                "op": 4,
                "d": {
                    "guild_id": str(guild_id),
                    "channel_id": str(channel_id),
                    "self_mute": False,
                    "self_deaf": False,
                },
            }
        )
        result = json.loads(await event)
        print(result)
        await inter.followup.send(result, ephemeral=True)

    @app_commands.command()
    async def disconnect(self, inter: Interaction):
        pass


class TTSDictinary(commands.GroupCog, name='dict'):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command()
    async def add_word(self, inter: Interaction, before_word: str, after_word: str):
        pass

    @app_commands.command()
    async def remove_word(self, inter: Interaction, delete_word: str):
        pass

    @app_commands.command()
    async def edit_word(self, word: str, new_word: str):
        pass

    @app_commands.command()
    async def show_dict(self, inter: Interaction):
        pass


async def setup(bot: VocalizeCore):
    await bot.add_cog(TextToSpeach(bot))
    await bot.add_cog(TTSDictinary(bot))
