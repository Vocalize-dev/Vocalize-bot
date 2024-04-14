from discord.ext import commands
from discord import Intents, LoginFailure
from glob import glob
from logging import getLogger
import traceback

LOG = getLogger(__name__)


class VocalizeCore(commands.Bot):
    def __init__(self, token: str, intents: Intents= Intents.default()):
        self.token = token
        super().__init__(command_prefix='+', intents=intents)

    async def setup_hook(self):
        extensions = glob('vocalize-bot/cogs/*.py')
        for extension in extensions:
            if extension.startswith('_'):
                LOG.info(f'loading {extension} was skipped.')
            else:
                LOG.info(f'loading extension {extension}')
                try:
                    self.load_extension(extension)
                except Exception as e:
                    LOG.error(f'failed to load extension {extension}: {e}')
                finally:
                    LOG.info(f'loaded extension {extension}')
        LOG.info(f'loaded {len(extensions)} extensions')
        await self.tree.sync()

    async def run(self, is_reconnect: bool= True):
        try:
            await self.start(self.token, reconnect=is_reconnect)

        except KeyboardInterrupt:
            LOG.info('Shutdown...')

        except LoginFailure:
            LOG.error('TOKEN is invalid')

        else:
            LOG.error(traceback.format_exc())
